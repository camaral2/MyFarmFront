## Commnad of Git
```
git config --global user.email "you@email.com"
git config --global user.name "Your name""

git add bees.txt
git commit -m "Added bees.txt"
git branch -M main
git remote add origin http:\\....git

git push -u origin main
```

pip install flask
pip install requests
pip install PyJWT


Dados climáticos
https://hgbrasil.com/apis/planos

Fase da Lua
https://api.farmsense.net/v1/moonphases/?d=1742932763

python3 main.py

docker network create myfarm_net

Dev:
docker compose --profile dev up --build
docker compose --profile dev up --build -d

Prod:
docker compose --profile prod up --build

-----
python3 -m venv .venv
source .venv/bin/activate

pip freeze > requirements.txt
pip install -r requirements.txt

## Deploy na Vercel
1. Crie um projeto na Vercel apontando para a pasta `MyFarmFront`.
2. Garanta que a Vercel use o arquivo `vercel.json` criado neste diretório.
3. Configure as variáveis de ambiente:
   - `API_URL` (URL pública do projeto `MyFarm` na Vercel)
   - `SECRET_KEY`
4. Faça o deploy.
