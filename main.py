# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import ProdutoDB
from models import LivroDB
from schemas import ProdutoCreate, ProdutoResponse
from schemas import LivroCreate, LivroResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List



Base.metadata.create_all(bind=engine) # cria as tabelas, se ainda não existirem
app = FastAPI()

app.add_middleware(
 CORSMiddleware,
 allow_origins=['*'],
 # em produção, restringir para o domínio real do front-end
 allow_methods=['*'],
 allow_headers=['*'],
)


@app.get('/produtos', response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
     return db.query(ProdutoDB).all()

@app.post('/produtos', response_model=ProdutoResponse, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = ProdutoDB(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto


# GET /produtos/{id} -> retorna um único produto pelo id
@app.get('/produtos/{produto_id}', response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
     produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
     if produto is None:
          raise HTTPException(status_code=404, detail='Produto não encontrado')
     return produto

# DELETE /produtos/{id} -> remove um produto do banco de dados
@app.delete('/produtos/{produto_id}', status_code=204)
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
     produto = db.query(ProdutoDB).filter(ProdutoDB.id ==produto_id).first()
     if produto is None:
       raise HTTPException(status_code=404, detail='Produto não encontrado')
     db.delete(produto)
     db.commit()
     return('Produto Excluido')

# PUT /produtos/{id} -> atualiza um produto existente no banco
@app.put('/produtos/{produto_id}', response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, dados: ProdutoCreate, db:
     Session = Depends(get_db)):
     produto = db.query(ProdutoDB).filter(ProdutoDB.id ==
     produto_id).first()
     if produto is None:
          raise HTTPException(status_code=404, detail='Produto não encontrado')
     produto.nome = dados.nome
     produto.preco = dados.preco
     produto.quantidade = dados.quantidade
     db.commit()
     db.refresh(produto)
     return produto


# Exercicio----------------------------------------------------------------------------------------------

@app.get('/livros', response_model=List[LivroResponse])
def listar_livros(db: Session = Depends(get_db)):
     return db.query(LivroDB).all()


@app.post('/livros', response_model=LivroResponse, status_code=201)
def criar_livro(livro:LivroCreate, db: Session = Depends(get_db)):
    novo_livro = LivroDB(**livro.dict())
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro


# DELETE /produtos/{id} -> remove um produto do banco de dados
@app.delete('/livros/{livros_id}', status_code=204)
def remover_livros(livros_id: int, db: Session = Depends(get_db)):
     livros= db.query(LivroDB).filter(LivroDB.id ==livros_id).first()
     if livros is None:
       raise HTTPException(status_code=404, detail='Livro não encontrado')
     db.delete(livros)
     db.commit()
     return('Livro Excluido')

# PUT /produtos/{id} -> atualiza um produto existente no banco
@app.put('/produtos/{livros_id}', response_model=LivroResponse)
def atualizar_produto(produto_id: int, dados: LivroCreate, db:
     Session = Depends(get_db)):
     livros = db.query(LivroDB).filter(LivroDB.id ==livros_id).first()
     if livros is None:
          raise HTTPException(status_code=404, detail='Livro não encontrado')
     livros.titulo = dados.titulo
     livros.autor = dados.autor
     livros.ano_publicacao = dados.ano_publicacao
     livros.preco = dados.preco
     
     db.commit()
     db.refresh(livros)
     return livros