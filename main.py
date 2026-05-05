import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")

EMAIL_SENHA = os.getenv("EMAIL_SENHA")

EMAIL_DESTINOS = os.getenv("EMAIL_DESTINOS")

if not EMAIL_REMETENTE or not EMAIL_SENHA or not EMAIL_DESTINOS:
    raise EnvironmentError(
        "Secrets de e-mail não configurados no GitHub."
    )

URL = "https://unicadata.com.br/listagem.php?idMn=63"
ARQUIVO_CONTROLE = "ultimo_link.txt"

def pegar_pdf_recente():
    r = requests.get(URL, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    for link in soup.find_all("a", href=True):
        href = link["href"].lower()
        texto = link.text.lower()

        if ".pdf" in href and (
            "quinzena" in texto or "safra" in texto or "centro-sul" in texto
        ):
            if not href.startswith("http"):
                return "https://unicadata.com.br/" + href.lstrip("/")
            return link["href"]
    return None


def baixar_pdf(url):
    nome = url.split("/")[-1]
    r = requests.get(url, timeout=30)
    r.raise_for_status()

    with open(nome, "wb") as f:
        f.write(r.content)

    return nome


def enviar_email(arquivo, link):
    destinatarios = EMAIL_DESTINOS.split(",")

    msg = EmailMessage()
    msg["Subject"] = "Nova quinzena UNICA disponível"
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = ", ".join(destinatarios)

    msg.set_content(f"""
Nova atualização da UNICA disponível.

Link:
{link}
""")

    with open(arquivo, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=arquivo
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_REMETENTE, EMAIL_SENHA)
        smtp.send_message(msg)


def main():
    link_atual = pegar_pdf_recente()
    if not link_atual:
        print("Nenhum PDF encontrado.")
        return

    ultimo = ""
    if os.path.exists(ARQUIVO_CONTROLE):
        with open(ARQUIVO_CONTROLE, "r") as f:
            ultimo = f.read().strip()

    if link_atual != ultimo:
        print("Novo PDF encontrado!")
        arquivo = baixar_pdf(link_atual)
        enviar_email(arquivo, link_atual)

        with open(ARQUIVO_CONTROLE, "w") as f:
            f.write(link_atual)
    else:
        print("Sem atualização.")


if __name__ == "__main__":
    main()

  
                        
    

  
