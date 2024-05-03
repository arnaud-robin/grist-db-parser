import grist
from functions import *       # global uppercase functions
import datetime, math, re     # modules commonly needed in formulas


@grist.UserTable
class All_Products:
  Size = grist.Choice()
  Product_Variant_Description = grist.Reference('Product_Variant')

  @grist.formulaType(grist.Text())
  def Product(rec, table):
    return rec.Brand.Product

  @grist.formulaType(grist.Choice())
  def Stock_Alert(rec, table):
    if rec.In_Stock + rec.QTY_on_Order > 5:
      return "In Stock"
    if rec.In_Stock + rec.QTY_on_Order > 0:
      return "Low Stock"
    else:
      return "OUT OF STOCK"

  @grist.formulaType(grist.Reference('Add_Products'))
  def Brand(rec, table):
    return rec.Product_Variant_Description.Name_Brand

  @grist.formulaType(grist.Reference('Color'))
  def Color(rec, table):
    return rec.Product_Variant_Description.Color

  @grist.formulaType(grist.Numeric())
  def In_Stock(rec, table):
    return rec.Received-rec.Sold if rec.Sold or rec.Received else 0 


  @grist.formulaType(grist.Numeric())
  def Received(rec, table):
    return SUM(Incoming_Order_Line_Items.lookupRecords(SKU=rec.id).Received_Qty)


  @grist.formulaType(grist.Text())
  def SKU(rec, table):
    return rec.Brand.Brand_Code+"-"+rec.Color.Code+"-"+rec.Size

  @grist.formulaType(grist.Numeric())
  def Sold(rec, table):
    return SUM(Outgoing_Orders.lookupRecords(Line_Item_SKU=rec.id).Lineitem_Quantity)

  @grist.formulaType(grist.Numeric())
  def Cost_per_Unit(rec, table):
    return rec.Product_Variant_Description.Cost_per_Unit

  @grist.formulaType(grist.Numeric())
  def QTY_on_Order(rec, table):
    return SUM(Incoming_Order_Line_Items.lookupRecords(SKU=rec.id).Qty)-SUM(Incoming_Order_Line_Items.lookupRecords(SKU=rec.id).Received_Qty)



@grist.UserTable
class Add_Products:
  Brand_Code = grist.Text()
  Name_Brand = grist.Choice()
  Product = grist.Text()


@grist.UserTable
class Color:
  Code = grist.Text()
  Color = grist.Choice()


@grist.UserTable
class Incoming_Orders:

  def _default_Status(rec, table, value, user):
    return "Order Placed"
  Status = grist.Choice()

  def _default_Tanggal_Diterima(rec, table, value, user):
    if rec.Status == "Received":
      return NOW()
  Tanggal_Diterima = grist.Date()
  Order_Date = grist.Date()

  @grist.formulaType(grist.Numeric())
  def Total(rec, table):
    return SUM(Incoming_Order_Line_Items.lookupRecords(Order_Number=rec.id).Total)

  @grist.formulaType(grist.Date())
  def Order_Number(rec, table):
    return rec.Order_Date


@grist.UserTable
class Product_Variant:
  Name_Brand = grist.Reference('Add_Products')
  Color = grist.Reference('Color')
  Photos = grist.Attachments()
  Cost_per_Unit = grist.Numeric()

  def Product(rec, table):
    return rec.Name_Brand.Product

  def Color_Code(rec, table):
    return rec.Color.Code

  @grist.formulaType(grist.Text())
  def Description(rec, table):
    return "{} {}".format(rec.Product, rec.Color.Color)


@grist.UserTable
class Incoming_Order_Line_Items:
  Order_Number = grist.Reference('Incoming_Orders')
  SKU = grist.Reference('All_Products')
  Qty = grist.Numeric()

  @grist.formulaType(grist.Numeric())
  def Total(rec, table):
    return rec.Cost_per_Unit*rec.Qty

  @grist.formulaType(grist.Numeric())
  def Received_Qty(rec, table):
    if rec.Order_Number.Status =='Received':
      return rec.Qty
    else:
      return None

  @grist.formulaType(grist.Numeric())
  def Cost_per_Unit(rec, table):
    return rec.SKU.Cost_per_Unit


@grist.UserTable
class Outgoing_Orders:
  Name = grist.Text()
  Phone = grist.Text()
  Email = grist.Text()

  def _default_Financial_Status(rec, table, value, user):
    if rec.Amount_Paid == 0:
      return "Unpaid"
    if rec.Total == rec.Amount_Paid:
      return "Paid in Full"
    if rec.Total > rec.Amount_Paid > 0:
      return "Partial Payment"
  Financial_Status = grist.Choice()
  Order_ID = grist.Numeric()
  Paid_At = grist.Date()
  Fulfillment_Status = grist.Choice()
  Currency = grist.Text()
  Subtotal = grist.Numeric()
  Taxes = grist.Numeric()
  Shipping = grist.Numeric()
  Discount_Code = grist.Text()
  Shipping_Method = grist.Choice()
  Discount_Amount = grist.Numeric()
  Amount_Paid = grist.Numeric()
  Created_At = grist.DateTime('America/Chicago')
  Lineitem_Quantity = grist.Numeric()
  Line_Item_SKU = grist.Reference('All_Products')
  Billing_Name = grist.Text()
  Billing_Address_1 = grist.Text()
  Billing_Street = grist.Text()
  Billing_City = grist.Text()
  Billing_Address_2 = grist.Text()
  Billing_State = grist.Text()
  Billing_Zip = grist.Numeric()
  Billing_Country = grist.Text()
  Billing_Phone = grist.Text()
  Shipping_Name = grist.Text()
  Shipping_Street = grist.Text()
  Shipping_Address_1 = grist.Text()
  Shipping_Address_2 = grist.Text()
  Shipping_City = grist.Text()
  Shipping_State = grist.Text()
  Shipping_Zip = grist.Text()
  Shipping_Country = grist.Text()
  Shipping_Phone = grist.Text()
  Notes = grist.Text()
  Cancelled_At = grist.Text()
  Payment_Method = grist.Text()
  Refunded_Amount = grist.Text()

  @grist.formulaType(grist.Numeric())
  def Total(rec, table):
    return rec.Subtotal+rec.Shipping+rec.Taxes-rec.Discount_Amount

  def Line_item_Name(rec, table):
    return rec.Line_Item_SKU.Product

  @grist.formulaType(grist.Numeric())
  def Line_Item_Price(rec, table):
    return rec.Line_Item_SKU.Cost_per_Unit

  @grist.formulaType(grist.Numeric())
  def Outstanding_Balance(rec, table):
    if rec.Financial_Status == "Unpaid":
      return rec.Total
    if rec.Financial_Status == "Paid in Full":
      return "0.00"
    if rec.Financial_Status == "Partial Payment":
      return rec.Total - rec.Amount_Paid


@grist.UserTable
class GristDocTour:
  Title = grist.Text()
  Body = grist.Text()
  Placement = grist.Text()
  LocationCell = grist.Text()

  @grist.formulaType(grist.Text())
  def Location(rec, table):
    return SELF_HYPERLINK()+rec.LocationCell
