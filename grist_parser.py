import re

def convert_type(grist_type, formula=False):
    # Determine the base type and potential reference information
    if "Text" in grist_type:
        base_type = "varchar"
    elif "Int" in grist_type:
        base_type = "integer"
    elif "Numeric" in grist_type:
        base_type = "numeric"
    elif "Date" in grist_type:
        base_type = "date"
    elif "ChoiceList" in grist_type:
        base_type = "multiple_choice"
    elif "Choice" in grist_type:
        base_type = "single_choice"
    elif "Reference" in grist_type:
        ref_table = re.search(r"'(\w+)'", grist_type)
        if "ReferenceList" in grist_type:
            ref_info = f"[ref: <> {ref_table.group(1)}.id]" if ref_table else ""
            base_type = "integer_list"
        else:
            ref_info = f"[ref: > {ref_table.group(1)}.id]" if ref_table else ""
            base_type = "integer"
    elif "Attachments" in grist_type:
        base_type = "file"
    else:
        base_type = "varchar"

    final_type = base_type
    if formula:
        final_type = f'"formula[{base_type}]"'
    if 'ref_info' in locals():
        return final_type+" "+ref_info
    return final_type

def parse_grist_code(file_path):
    tables = {}
    current_class = None
    current_formula_type = '"formula[default]"'

    with open(file_path, 'r') as file:
        for line in file:
            class_match = re.search(r'class (\w+):', line)
            field_match = re.search(r'(\w+) = grist\.(\w+)', line)
            formula_match = re.search(r'def (?!_default_|gristHelper_)(\w+)', line)
            formula_type_match = re.search(r'grist.formulaType\(grist\.(.+)\)', line)

            if formula_match:
                field_name = formula_match.group(1)
                tables[current_class].append((field_name, current_formula_type))
                current_formula_type = '"formula[default]"'
            elif formula_type_match:
                current_formula_type = convert_type(formula_type_match.group(1), formula=True)
            elif class_match:
                new_class = class_match.group(1)
                if new_class == "_Summary":
                    current_class += "_Summary"
                else:
                    current_class=new_class
                tables[current_class] = []
            elif field_match and current_class:
                field_name, grist_type = map(str.strip, line.split('='))
                sql_type = convert_type(grist_type)
                tables[current_class].append((field_name, sql_type))

    # Generating DBML output
    dbml_output = []
    for table_name, fields in tables.items():
        dbml_output.append(f"Table {table_name} {{")
        dbml_output.append("  id integer [primary key]")
        for field_name, sql_type in fields:
            dbml_output.append(f"  {field_name} {sql_type}")
        dbml_output.append("}\n")

    return "\n".join(dbml_output)

def write_dbml_to_file(dbml_code, output_path):
    with open(output_path, 'w') as file:
        file.write(dbml_code)
