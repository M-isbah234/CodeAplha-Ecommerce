import os
import glob

search_dir = 'c:\\Users\\AAMIR SHAMSI\\Agentic_Ai\\CodeAlpha\\ecommerce_site'
html_files = glob.glob(search_dir + '/**/*.html', recursive=True)

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '$' in content:
        # Avoid replacing variables in JS/jQuery if any, but since it's Django templates:
        new_content = content.replace('$', 'PKR ')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {file_path}')

# Update admin.py
admin_file = os.path.join(search_dir, 'shop', 'admin.py')
with open(admin_file, 'r', encoding='utf-8') as f:
    content = f.read()
if '$' in content:
    with open(admin_file, 'w', encoding='utf-8') as f:
        f.write(content.replace('Total ($)', 'Total (PKR)'))
    print(f'Updated {admin_file}')
