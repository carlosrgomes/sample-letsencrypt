Usando Let’s Encrypt no App Engine
---
[Let’s Encrypt](https://letsencrypt.org/) é um CA (Certificate Authority) open, ou seja, totalmente free, com ele podemos gerar certificados digitais (SSL) para websites, microservices entre outros casos de uso.

Tecnologias
---
Este artigo está utilizando as seguintes tecnologias:

  - [Let’s Encrypt](https://letsencrypt.org/)
  - [Python](https://www.python.org/)
  - [Flask](http://flask.pocoo.org/)
  - [Google App Engine](https://cloud.google.com/appengine/)
  
 Pré Requisitos
  ---
 Para executar o exemplo do Let's Encrypt você vai precisar de um projeto no [Google Cloud Platform](https://console.cloud.google.com) e ter instalado o [Google Cloud SDK](https://cloud.google.com/sdk/downloads?hl=pt-br).
 Para saber mais sobre como criar um projeto no Googe Cloud clique [aqui](https://cloud.google.com/sdk/downloads?hl=pt-br) e siga as instruções para criar seu projeto.
 
Digite no terminal do seu sistema operacional
```
gcloud init
```
Siga as instruções e logue no seu projeto do GCP (Google Cloud Platform).

Faça o download do repositório com o código fonte:

```
https://github.com/carlosrgomes/sample-letsencrypt.git
```

Entre no diretório sample-letsencrypt e faça o deploy da sua aplicação no App Engine com o comando:
```
gcloud app deploy
```

Faça o download do [Let’s Encrypt](https://letsencrypt.org/) em outro diretório:

```
git clone https://github.com/letsencrypt/letsencrypt
cd letsencrypt
./letsencrypt-auto --help
```

Configurando seu domínio
---
No Console do GCP temos que entrar no Settings do App Engine conforme pode observar na imagem.


![App Engine Settings](images/appenginesettings.png)

Siga as intruções e configure o domínio de sua aplicação. No final das configuraes você será capaz de entrar no site através do configurado. Por exemplo quando escrevi esse artigo o domínio da minha aplicação ficou acessível através do link:
[http://easycloudbr.com/](http://easycloudbr.com/)

![App Engine Dominio](images/dominio1.png)

Gerando o SSL
---
Dentro da pasta letsencrypt vamos executar o comando

```bash
sudo ./letsencrypt-auto certonly --manual --email seuemail@email.com -d seudominio.com
```
Logo após esse comando o letencrpty vai apresentar a seguinte mensagem:

```
-------------------------------------------------------------------------------
NOTE: The IP of this machine will be publicly logged as having requested this
certificate. If you're running certbot in manual mode on a machine that is not
your server, please ensure you're okay with that.

Are you OK with your IP being logged?
-------------------------------------------------------------------------------
(Y)es/(N)o: Y

```
Confirme digitando "Y"

O [Let’s Encrypt](https://letsencrypt.org/) vai criar uma chave e um valor que você precisa utilizar no código da aplicação que deseja gerar o SSL.

Conforme pode observar no exemplo abaixo.

```
-------------------------------------------------------------------------------
Create a file containing just this data:

J_Y_SHt8Pcvd6aFDtvhvunP2z99YGJj8kDeDRpCU6xg.89n5ovJLN0aPGfXjM5TBFporRo0qvYDmO4nwmbvUxFk

And make it available on your web server at this URL:

http://easycloudbr.com/.well-known/acme-challenge/J_Y_SHt8Pcvd6aFDtvhvunP2z99YGJj8kDeDRpCU6xg

-------------------------------------------------------------------------------
Press Enter to Continue
Waiting for verification...
Cleaning up challenges
```
Nesse exemplo a chave será J_Y_SHt8Pcvd6aFDtvhvunP2z99YGJj8kDeDRpCU6xg e o valor J_Y_SHt8Pcvd6aFDtvhvunP2z99YGJj8kDeDRpCU6xg.89n5ovJLN0aPGfXjM5TBFporRo0qvYDmO4nwmbvUxFk

Vamos precisar alterar o arquivo main.py nele temos um contexto /.well-known/acme-challenge/<challenge> configurado como @app.route('/.well-known/acme-challenge/<challenge>') o [Let’s Encrypt](https://letsencrypt.org/) utiliza esse contexto para validar e gerar o certificado ssl. Você vai precisar substituir dentro do dict da função a chave e os valores gerados pelo [Let’s Encrypt](https://letsencrypt.org/) conforme o código:
  
```python
@app.route('/.well-known/acme-challenge/<challenge>')
def letsencrypt_check(challenge):
    challenge_response = {
        "chave_aqui":"valor_aqui",
        "chave_aqui":"valor_aqui"
    }
    return flask.Response(response= challenge_response[challenge], status=200, mimetype='text/plain')
```

Coformem os valores anteriomente citados o código ficaria assim:

```python
@app.route('/.well-known/acme-challenge/<challenge>')
def letsencrypt_check(challenge):
    challenge_response = {
        "J_Y_SHt8Pcvd6aFDtvhvunP2z99YGJj8kDeDRpCU6xg":"J_Y_SHt8Pcvd6aFDtvhvunP2777Jj8kDeDRpCU6xg.89n5ovJL777jM5TBFporRo0qvYDmO4nwmbvUxFk",
        "<challenge_token>":"<challenge_response>"
    }
    return flask.Response(response= challenge_response[challenge], status=200, mimetype='text/plain')
 ```
Salve o arquivo e faça um novo deploy na aplicação com o comando:

```
gcloud app deploy
```

Precione a tecla enter no terminal do [Let’s Encrypt](https://letsencrypt.org/) .

Se tudo estiver correto será apresentado uma mensagem parecida com a mensagem abaixo:

```
IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/easycloudbr.com/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/easycloudbr.com/privkey.pem
   Your cert will expire on 2018-07-18. To obtain a new or tweaked
   version of this certificate in the future, simply run
   letsencrypt-auto again. To non-interactively renew *all* of your
   certificates, run "letsencrypt-auto renew"
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le
```

Copie os arquivos que foram gerados par ao desktop ou alguma pasta com acesso de leitura e escrita:

```
cp /etc/letsencrypt/live/easycloudbr.com/fullchain.pem /home/suapasta/
cp /etc/letsencrypt/live/easycloudbr.com/privkey.pem /home/suapasta/
```

Voltando para o Settings do Console do App Engine clique na Aba SSL certificates, aqui você vai precisar fazer upload da chave pública que foi gerada pelo Let's Encrypt.

![App Engine SSL](images/ssl.png)

Na primeira opção (PEM encoded X.509 public key certificate) escolha o arquivo gerado com o nome fullchain.pem.
Feito isso sua tela vai carregar o certificado conforme a imagem:

![App Engine SSL](images/ssl2.png)

Na segunda opção (Unencrypted PEM encoded RSA private key) da tela do SSL do App Engine vamos precisar do private key, para obter as informações vamos precisar entrar na pasta onde você salvou o privkey.pem e executar o comando:

```
sudo openssl rsa -inform pem -in privkey.pem -outform pem
```

Será exibido a seguinte mensagem:

```
writing RSA key
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEApy8m1PqaDZPZDYjwjuArRV/YcXiBqDJqEvrOr+GXQwTsKX9x
g1D0RIBaHkOR3XNv4lERy4V4K+N5rk6tKVelylqqQNDAwfgoepZLfguXD8TvoUlo
82Gx949H/xW6vnUKYLCFpqrC0FiAN5tbNOWjbBUyHoOl/sOA/TCi1Gx0Kn66aQCv
l/Rg018PiSHy2o2Yrq14HrIhCvPnkQ7GAN1e+jdPjbi/wZIVCh1a/sl55ciwJjYk
GLkuXj4bXJvE0gTw9jLKonEdm/p/DrrQFjOL/JxIKM+sYqtOdRvZVH0Gt2gmD8H7
eqNpEWVMVhOJ4rccqc3wXr+B8Q/5fSpbFVzUFwIDAQABAoIBAEyUqLD+afq2MsKk
a6zGuot4r+iqTpoBHd27zVl7eJJWeuc3XYPNXVbThHRAd1x9OE7u27viU32nIWHa
4C8D2wmqJjqyZNl1FvWwSrxeCsBKcYnr2otBwQepNk1+YqBDdJF9ynrh1YMiRvkx
zMGaPxWPT/nyS+M7IqbX1H6Bf2THEm9mTlk3MMJ9a5IO8T6T19WyqjsrknBpppRp
v/dz8uo6xrgW9Dk0+vg4OZuyJTPE7eniUppdgfAqKvhDDCRMP/AK8oxYmtX95Li3
4eIWu07rqnepjU8W/EA6mHYG8hB380bBxxT+ABciTLfrJtRJrycOZruwIniI3cCx
w4ht48ECgYEA1jJaaXFtGAiVirlnbt/LImW30j0iCsrQhTxwQF0l+p26bqzb6AH9
zNGt9qmGt+gy6oTDf2Pjrz/gYY/ivzKk/SVjSaY5WKXjgN3w3FbSboQElKETiQ1M
qzhbMFKt5ZbEF8GL+8uAFvEqRB9KpC/IiNS2KPf6rVQy6NngrQNDa4kCgYEAx8/4
Zb2xh9BuUtgHtrkfHrXAQ/fSWZ58wy/hGkiBX/FDh8qKQiNO7wuNbYJs4G9cHFmT
JYlGF9FGeEClvvwvt9AJGDQZJSGKXa2PbidX2/bybHMQUI8DmiLw0YZvpy/nu8TW
rZcmJItivPJ2XDzwY93Yl0Dqb6PCcHDx198gOp8CgYALizMsM5y5itzkWRGl/BGq
jOjXP8wx4LRUOemizmJZm16M0GwZmOHgw/woKwLDrpPv56/RkcSXkU26dFK4Ezap
Hfa35Wl5yZb1PwDYHyXAJwVILVYsMLdNEwB3Hj2Y/gMbdKbirxj8I4svmLAhISIh
nbUjiBnOdZc4zWU6bc6YYQKBgQCsocQsst2lR7FppffUKND4SXNZxc1ZXJLSWJWV
jbspV1tPAPC+/5587XA9gwfqSIw+ei2lqpqCjW7jCoepIF1h5D1XSfvHltji4scf
FqLUCuGcTTV1RHqKO1Hw1MO2oK8IDaKkzAhKXprqQFl+i6/tuIge9hkWZ1fgqdRo
+//uZQKBgDzyPcUMui+3Y5XA5YaDDaAyGfpMC8i+X1GH5XeQwl99jtqfHRNTc22w
jKLyLPKU9hgpBMnJsnuyMykDvCrZJpyfd8wgDzsS2pjXWY218xIUCEl96+i7fsHw
j9dkLG8KOy0bSWgGffOHB0k/54vz0XWO+Wu7y6xhcPOtRHCp2lNe
-----END RSA PRIVATE KEY-----
```

Temos que copiar essa mensagem desde -----BEGIN RSA PRIVATE KEY----- até -----END RSA PRIVATE KEY----- e colar na segunda opção do SSL do App Engine conforme imagem:

![App Engine SSL](images/ssl3.png)

Clique no botão Upload. 
Parabéns você acabou de gerar um certificado válido para sua aplicação!

Você pode conferir seu certificado no site: 
[sslshopper](https://www.sslshopper.com/)

![App Engine SSL](images/ssl_shopper.png)







