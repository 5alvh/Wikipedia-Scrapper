import os
from datetime import datetime
from Managers.DbManager import dbService


class HTMLManager:
    def __init__(self):
        self.db = dbService()
        self.output_dir = "html_output"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_html(self, url_id, url_text):
        
        print("Generating HTML...")
        content_data = self.db.getContent(url_id)
        
        if not content_data:
            return {"success": False, "message": "No content found for this URL"}

        try:
            html_content = f"""<!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{url_text}</title>
            <style>
            body {{ 
            font-family: 'Segoe UI', Arial, sans-serif; 
            line-height: 1.6; 
            margin: 2rem;
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }}
        h1 {{ color: #8B4513; border-bottom: 2px solid #FFA500; }}
        .section {{ 
            margin-bottom: 2rem; 
            padding: 1rem; 
            border-left: 4px solid #FFA500;
            background-color: #f9f9f9;
            border-radius: 5px;
        }}
        .content-title {{ color: #4CAF50; margin-top: 1.5rem; }}
        p {{ margin: 0.5rem 0; font-size: 16px; }}
        ul {{ padding-left: 1.5rem; list-style-type: square; }}
        li {{ margin: 0.3rem 0; }}
        </style>
        </head>
        <body>
         <h1>{url_text}</h1>
        """

            current_section = None
            section_content = ""

            for title, content, content_type in content_data:
                print(content_type)  # Debugging output
                if " - " in title:
                    
                    main_title, section_title = title.split(" - ", 1)
                else:
                    section_title = title

                if section_title != current_section:
                    if current_section is not None:
                        html_content += section_content + "</div>\n"  
                    html_content += f"""
                    <div class="section">
                        <h2 class="content-title">{section_title}</h2>"""
                    current_section = section_title
                    section_content = ""  

                if content:
                    section_content += f"<p>{content}</p>\n"
                    

            if current_section is not None:
                html_content += section_content + "</div>\n"

            html_content += """
            </body>
            </html>
            """
            filename = f"wiki_scrapped_{url_id}.html"
            file_path = os.path.join(self.output_dir, filename)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            return {
                "success": True,
                "message": "HTML file generated successfully",
                "file_path": file_path
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error generating HTML: {str(e)}"
            }


