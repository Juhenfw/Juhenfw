import json
import re

def generate_project_markdown():
    with open('data/projects.json', 'r', encoding='utf-8') as f:
        projects = json.load(f)
        
    markdown = ""
    for p in projects:
        tech_stack = ", ".join([f"`{t}`" for t in p['tech']])
        markdown += f"- **[{p['title']}]({p['url']})**\n"
        markdown += f"  {p['description']} ({tech_stack})\n"
    return markdown

def generate_publication_markdown():
    try:
        # Membaca data dari file publikasi JSON yang baru
        with open('data/publications.json', 'r', encoding='utf-8') as f:
            publications = json.load(f)
            
        markdown = ""
        for pub in publications:
            title = pub.get('title', 'Untitled')
            year = pub.get('year', '')
            url = pub.get('url', '')
            
            # Membuat tombol badge jika URL tersedia
            if url:
                button = f"<a href='{url}' target='_blank'><img src='https://img.shields.io/badge/📖_View_Paper-F7768E?style=flat-square' alt='View Paper'/></a>"
            else:
                button = ""
                
            year_str = f" ({year})" if year else ""
            markdown += f"- **{title}**{year_str} {button}\n"
            
        return markdown if markdown else "- Belum ada data publikasi yang ditemukan.\n"
    
    except FileNotFoundError:
        return "- <!-- File data/publications.json tidak ditemukan! -->\n"
    except Exception as e:
        return f"- <!-- Error membaca file publikasi: {e} -->\n"

def update_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()

    # 1. Update Projects
    projects_md = generate_project_markdown()
    readme = re.sub(
        r'(<!-- START_SECTION:projects -->).*?(<!-- END_SECTION:projects -->)',
        f'\\1\n{projects_md}\\2',
        readme,
        flags=re.DOTALL
    )

    # 2. Update Publications (Sekarang membaca dari JSON)
    scholar_md = generate_publication_markdown()
    readme = re.sub(
        r'(<!-- START_SECTION:scholar -->).*?(<!-- END_SECTION:scholar -->)',
        f'\\1\n{scholar_md}\\2',
        readme,
        flags=re.DOTALL
    )

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme)

if __name__ == "__main__":
    update_readme()