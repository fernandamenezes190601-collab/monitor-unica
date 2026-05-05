import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

URL = "https://unicadata.com.br/listagem.php?idMn=63"

EMAIL = "turmabi2026@gmail.com"
SENHA = "Jacare@2026"
DESTINOS = ["fernanda.bmenenezes@saomartinho.com.br", "pedro.quirino@saomartinho.com.br", "giovanna.cordova@saomartinho.com.br", "pedro.abud@saomartinho.com.br"]

ARQUIVO_CONTROLE = "ultimo_link.txt"

def pegar_pdf_recente():
  r = requests.get(URL)
  soup = BeautifulSoup(r.text, "html.parser")
  
  links = soup.find_all("a", href=True)
  
  pdfs = []
  for link in links:
    href = link["href"].lower()
    texto = link.text.lower()

    if ".pdf" in href and ("quinzena" in texto or "safra" in texto or "centro-sul" in texto):
      if not href.startswith("http"):
        href = "https://unicadata.com.br/listagem.php?idMn=63" + href
        pdfs.append(href)
  if not pdfs:
    return None
  return pdfs[0]

def baixar_pdf(url):
  nome = url.split("/")[-1]
  r = requests.get(url)
  with open(nome, "wb") as f:
  f.write(r.content)
  return nome

def enviar_email(arquivo, link):
  msg = EmailMessage()
  msg["Subject"] = "Nova quinzena Unica disponível!"
  msg["From"] = EMAIL
  msg["To"] = ", ".join(DESTINOS)
  msg,set_content(f"""
  Nova atualização da Unica disponível.
  Link: {link}
  O arquivo está em anexo. 
  """)

  with open(arquivo,"rb") as f:
    msg.add_attachment(f.read(), maintype="application", subtype="pdf",filename=arquivo)
  with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL, SENHA)
    smtp.send_message(msg)

def main():
  link_atual = pegar_pdf_recente()
  if not link_atual:
    print("Nenhum PDF encontrado")
    return
  if os.path.exists(ARQUIVO_CONTROLE):
    with open(ARQUIVO_CONTROLE, "r") as f:
      ultimo = f.read()
  else:
    ultimo = ""

  if link_atual != ultimo:
    print("Novo PDF encontrado!")

    arquivo = baixar_pdf(link_atual)
    enviar_email(arquivo, link_atual)

    with open(ARQUIVO_CONTROLE, "w") as f:
      f.write(link_atual)

  else:
    print("Sem atualização.")

if _name__ == "_main_":
  main()

    
  
  
                        
    

  
