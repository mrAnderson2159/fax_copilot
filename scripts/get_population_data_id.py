import re

if __name__ == '__main__':
    with open('/Users/mr.anderson2159/zoolab/backend/app/population_data.py', 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines if 'new_fiend' in line]
        # Regex modificata per gestire apici singoli o doppi e spazi
        fiends = [re.search(r'new_fiend\s*\(\s*[\'"]([^\'"]+)[\'"]', line) for line in lines]
        fiend_names = [match.group(1) for match in fiends if match]

        for i, name in enumerate(fiend_names):
            if name == 'budino d':
                name = "budino d''acqua"
            print(f"UPDATE fiends SET id = {i + 1} WHERE name = '{name.lower()}';")
