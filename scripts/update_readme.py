import json
import re
from scholarly import scholarly

def generate_project_markdown():
    with open('data/projects.json', 'r') as f:
        projects = json.load(f)
        
    markdown = ""
    for p in projects:
        tech_stack = ", ".join([f"`{t}`" for t in p['tech']])
        markdown += f"- **[{p['title']}]({p['url']})**\n"
        markdown += f"  {p['description']} ({tech_stack})\n"
    return markdown

def get_scholar_publications(author_id, max_pubs=5):
    try:
        author = scholarly.search_author_id(author_id)
        scholarly.fill(author, sections=['publications'])
        
        markdown = ""
        for i, pub in enumerate(author['publications']):
            if i >= max_pubs:
                break
            title = pub['bib'].get('title', 'Untitled')
            year = pub['bib'].get('pub_year', 'N/A')
            
            # --- BAGIAN BARU: Membuat Link Tautan ---
            # Mengambil ID spesifik artikel untuk membuat direct link
            pub_id = pub.get('author_pub_id', '')
            
            if pub_id:
                # Format URL standar Google Scholar untuk melihat sitasi spesifik
                url = f"https://scholar.google.com/citations?view_op=view_citation&user={author_id}&citation_for_view={pub_id}"
                
                # Desain tombol menggunakan Markdown & HTML (pilih salah satu style)
                # Style Badge:
                button = f"<a href='{url}' target='_blank'><img src='https://img.shields.io/badge/📖_View_Paper-F7768E?style=flat-square' alt='View Paper'/></a>"
            else:
                button = ""
                
            # Menggabungkan ke format markdown README
            markdown += f"- **{title}** ({year}) {button}\n"
            
        return markdown if markdown else "- Belum ada data publikasi yang ditemukan.\n"
    except Exception as e:
        print(f"Error fetching scholar data: {e}")
        return "- <!-- Gagal menarik data Scholar saat eksekusi terakhir. Cek log Actions. -->\n"

def update_readme():
    with open('README.md', 'r') as f:
        readme = f.read()

    # 1. Update Projects
    projects_md = generate_project_markdown()
    readme = re.sub(
        r'(<!-- START_SECTION:projects -->\n).*?(<!-- END_SECTION:projects -->)',
        f'\\1{projects_md}\n\\2',
        readme,
        flags=re.DOTALL
    )

    # 2. Update Google Scholar (Menggunakan ID Anda: 7VxM9hwAAAAJ)
    scholar_id = "7VxM9hwAAAAJ" 
    scholar_md = get_scholar_publications(scholar_id, max_pubs=3)
    readme = re.sub(
        r'(<!-- START_SECTION:scholar -->\n).*?(<!-- END_SECTION:scholar -->)',
        f'\\1{scholar_md}\n\\2',
        readme,
        flags=re.DOTALL
    )

    with open('README.md', 'w') as f:
        f.write(readme)

if __name__ == "__main__":
    update_readme()