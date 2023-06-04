# Para instalar as dependências necessárias utilize no terminal o comando abaixo:
# pip install requests pyaudio SpeechRecognition pyttsx3 Pillow pyautogui speedtest-cli

import os.path
import subprocess
import requests
import speech_recognition as sr
import pyttsx3
import pyautogui
import datetime
import webbrowser
import speedtest
import json

def select_voice(voices):
    for voice in voices:
        if "pt-br" in voice.id.lower() and ("maria" in voice.id.lower() or "zira" in voice.id.lower()):
            return voice

    for voice in voices:
        if "maria" in voice.id.lower() or "zira" in voice.id.lower():
            return voice

    return voices[0]


friday_voice = pyttsx3.init()
friday_voice.setProperty("rate", 240)
friday_voice.setProperty("volume", 1.0)
voices = friday_voice.getProperty('voices')
voice = select_voice(voices)
friday_voice.setProperty('voice', voice.id)

oraculo_url = "https://api.openai.com/v1/chat/completions"
oraculo_key = "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"
oraculo_model = "gpt-4"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + oraculo_key
}

microfone = sr.Microphone()
reconhecedor = sr.Recognizer()

comando_inicial = "ok sexta-feira"
resposta_padrao = "Sim, mestre. O que posso fazer?"


def pedir_ao_oraculo(pedido):
    data = {
        "model": oraculo_model,
        "messages": [{"role": "user", "content": f"{pedido}"}],
        "temperature": 1.0
    }

    response = requests.post(oraculo_url, json=data, headers=headers)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return "Desculpe, o oraculo está em reunião nesse momento, podemos tentar novamente mais tarde"

    content = response.json()['choices'][0]['message']['content']
    return content


def falar_texto(texto):
    friday_voice.say(texto)
    friday_voice.runAndWait()


def cadastrar_evento():
    print("Ok, qual evento devo cadastrar ?")
    falar_texto("Ok, qual evento devo cadastrar ?")

    while True:
        try:
            audio = reconhecedor.listen(microfone)
            evento = reconhecedor.recognize_google(audio, language="pt")

            modo = "w"
            contador_evento = 0
            filename = "arquivo.txt"

            if os.path.exists(filename):
                modo = "a"
                with open(filename, "r") as file:
                    contador_evento = sum(1 for _ in file)

            with open(filename, modo) as file:
                file.write(evento + "\n");

            fala = f"{contador_evento+1}° evento, {evento}, cadastrado com sucesso"
            print(fala)
            falar_texto(fala)

            break

        except sr.UnknownValueError:
            print("Aguardando evento...")


def ler_agenda():
    nome_arquivo = "arquivo.txt"

    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "r") as arquivo:
            conteudo = arquivo.read()

            if (conteudo == ""):
                print("Não há eventos cadastrados")
                falar_texto("Não há eventos cadastrados")
            else:
                print(f"Há os seguintes eventos na agenda: {conteudo}")
                falar_texto(f"Há os seguintes eventos na agenda: {conteudo}")
    else:
        print("Não há eventos cadastrados")
        falar_texto("Não há eventos cadastrados")


def abrir_calculadora():
    print("Abrindo a calculadora")
    falar_texto("Abrindo a calculadora")
    subprocess.run(["calc.exe"])


def que_dia_e_hoje():
    data_hora_atual = datetime.datetime.now()
    dia_semana = data_hora_atual.weekday()
    dias_semana = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']
    nome_dia_semana = dias_semana[dia_semana]
    data_formatada = data_hora_atual.strftime('%d/%m/%Y')

    print(f"Hoje é {nome_dia_semana}, {data_formatada}")
    falar_texto(f"Hoje é {nome_dia_semana}, {data_formatada}")


def o_que_eh():
    print("Faça a pergunta e eu a levarei para o oráculo")
    falar_texto("Faça a pergunta e eu a levarei para o oráculo")

    while True:
        try:
            audio = reconhecedor.listen(microfone)
            pedido = reconhecedor.recognize_google(audio, language="pt")

            resposta = pedir_ao_oraculo(
                f"Você é um assistente como a alexa que se chama sexta-feira, então muito resumidamente responda: {pedido}")
            print(resposta)
            falar_texto(resposta)

            break

        except sr.UnknownValueError:
            print("Aguardando pergunta...")



def obter_clima_atual():
    url = "https://api.openweathermap.org/data/2.5/weather?q=são%20paulo&appid=224fbd4368ef3abe4eecebcf90e6ddea&lang=pt_br"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temperatura_minima = data["main"]["temp_min"] - 273.15
        temperatura_maxima = data["main"]["temp_max"] - 273.15
        descricao_clima = data["weather"][0]["description"]
        possibilidade_chuva = "com" if "rain" in data else "sem"

        resposta = f"Hoje está previsto mínimo de {str(temperatura_minima).split('.')[0]} graus e máxima de {str(temperatura_maxima).split('.')[0]} graus, {possibilidade_chuva} possibilidade de chuva. O clima está {descricao_clima}."
        print(resposta)
        falar_texto(resposta)
    else:
        return "Não foi possível obter as informações do clima no , podemos tentar mais tarde."



def tirar_print():
    agora = datetime.datetime.now()
    nome_arquivo = agora.strftime("%Y_%m_%d_%H_%M_%S") + '.png'
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(os.path.join(os.getcwd(), nome_arquivo))
        print("O print foi salvo no diretório onde estou armazenada")
        falar_texto("O print foi salvo no diretório onde estou armazenada")

    except Exception as e:
        print("Ocorreu um erro ao tirar o print:", str(e))
        print("Fui incapaz de tirar print nesse momento, tente novamente")
        falar_texto("Fui incapaz de tirar print nesse momento, tente novamente")


def tocar_musica():
    webbrowser.open('https://www.youtube.com/watch?v=6iFbuIpe68k')


def obter_cotacao_dolar():
    response = requests.get("http://economia.awesomeapi.com.br/json/last/USD-BRL")

    if response.status_code == 200:
        dados = json.loads(response.text)
        valor_em_reais = dados["USDBRL"]["bid"]
        print(f"O valor do dólar hoje é: R${valor_em_reais}")
        falar_texto(f"O valor do dólar hoje é: R${valor_em_reais}")
    else:
        print("O mercado financeiro está uma loucura e não foi possível obter a cotação do dólar agora.")
        falar_texto("O mercado financeiro está uma loucura e não foi possível obter a cotação do dólar agora.")


def velocidade_internet():
    s = speedtest.Speedtest()
    print("Iniciando teste de velocidade da internet... Aguarde!")
    s.get_best_server()

    download_speed = s.download()
    v_download = f"Velocidade de Download: {download_speed / 1e6:.2f} Mbps"

    upload_speed = s.upload()
    v_upload = f"Velocidade de Upload: {upload_speed / 1e6:.2f} Mbps"

    ping = s.results.ping
    t_ping = f"Ping: {str(ping).split('.')[0]} ms"

    print(v_download)
    print(v_upload)
    print(t_ping)
    falar_texto(f"Os testes resultaram em: {v_download}, {v_upload} e {t_ping}")


def reiniciar_computador():
    print("Reiniciando o sistema")
    falar_texto("Reiniciando o sistema")
    os.system("shutdown /r  /t 10")


def desligar_computador():
    print("Desligando o sistema")
    falar_texto("Desligando o sistema")
    os.system("shutdown /s /f /t 10")


comandos = {
    "cadastrar evento na agenda": cadastrar_evento,
    "ler agenda": ler_agenda,
    "reiniciar computador": reiniciar_computador,
    "desligar computador": desligar_computador,
    "que dia é hoje": que_dia_e_hoje,
    "pergunta": o_que_eh,
    "clima": obter_clima_atual,
    "calculadora": abrir_calculadora,
    "print": tirar_print,
    "dólar": obter_cotacao_dolar,
    "velocidade da internet": velocidade_internet,
    "música": tocar_musica
}

def main():
    with microfone as mic:
        print("Iniciando sistema...")
        while True:
            reconhecedor.adjust_for_ambient_noise(mic)
            print("Aguardando comando: Ok sexta feira")

            try:
                audio = reconhecedor.listen(mic)
                primeiro_comando = reconhecedor.recognize_google(audio, language="pt")

                if comando_inicial in primeiro_comando:
                    print(resposta_padrao)
                    falar_texto(resposta_padrao)

                    aguardar_comando = True
                    while aguardar_comando:
                        try:
                            audio = reconhecedor.listen(mic)
                            pedido = reconhecedor.recognize_google(audio, language="pt")
                            print(f"Fala reconhecida: {pedido}")

                            comando_encontrado = False
                            for comando, funcao in comandos.items():
                                if comando in pedido.lower():
                                    comando_encontrado = True
                                    try:
                                        funcao()
                                        aguardar_comando = False
                                        break
                                    except Exception as e:
                                        print(f"Ocorreu um erro ao executar a função: {e}")
                                        falar_texto(f"Ocorreu um erro ao executar a função: {e}")
                            if not comando_encontrado:
                                print("Comando desconhecido. Por favor, tente novamente.")
                                falar_texto("Comando desconhecido. Por favor, tente novamente.")

                        except sr.UnknownValueError:
                            print("Não foi possível reconhecer o pedido. Por favor, tente novamente.")
                else:
                    print(f"Fala reconhecida: {primeiro_comando}")
            except sr.UnknownValueError:
                print("Não foi possível reconhecer o comando inicial. Por favor, tente novamente.")


if __name__ == '__main__':
    main()
