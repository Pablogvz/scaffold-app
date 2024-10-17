# migration_generator.py
from datetime import datetime

class MigrationGenerator:
    def generate_migration_file(self, model, columns, table_name):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        migration_name = f"create_{model.lower()}"
        filename = f"{timestamp}_{migration_name}.rb"

        # Adjust the column strings to include null: false, foreign_key: true for references
        columns_str = ""
        for col_name, col_type in columns:
            if col_type == "references":
                columns_str += f"        t.references :{col_name}, null: false, foreign_key: true\n"
            else:
                columns_str += f"        t.{col_type} :{col_name}\n"

        columns_str += "        t.datetime :deleted_at\n"
        columns_str += "        t.string :updated_by\n"
        columns_str += "        t.string :created_by\n"

        migration_content = f"""
  def up
    unless table_exists?(:{table_name})
      create_table :{table_name} do |t|
{columns_str}

        t.timestamps
      end
    end
  end

  def down
    drop_table :{table_name} if table_exists?(:{table_name})
  end
"""

        return migration_content
