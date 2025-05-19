
# Sistema de Gestão de Aeroporto (Backend)

Este projeto tem como objetivo desenvolver uma aplicação backend que simule o sistema de gestão de um aeroporto. O sistema deve expor rotas HTTP para o gerenciamento de voos, passageiros e portões de embarque.

## 📦 Entidades Principais

### 1. Passageiro

* `id`: Identificador único
* `nome`: Nome completo
* `cpf`: CPF (deve ser válido e único)
* `vooId`: Referência ao voo
* `statusCheckIn`: `"pendente"` ou `"realizado"`

### 2. Voo

* `id`: Identificador único
* `numeroVoo`: Código do voo
* `origem`: Local de origem
* `destino`: Local de destino
* `dataHoraPartida`: Data e hora da partida
* `portaoId`: Referência ao portão de embarque
* `status`: `"programado"`, `"embarque"`, `"concluído"`

### 3. Portão de Embarque

* `id`: Identificador único
* `codigo`: Ex: `"A5"`
* `disponivel`: `true` ou `false`

## ✅ Funcionalidades Obrigatórias

### 1. CRUD

* Operações completas de **Create**, **Read**, **Update** e **Delete** para passageiros e voos.

### 2. Validações

* Validação básica e coerente de todos os atributos.
* CPF deve ser válido e único por passageiro.
* Um portão só pode ser vinculado a um voo por vez.
* Passageiros só podem fazer check-in se o voo estiver com status `"embarque"`.

### 3. Regras de Negócio

* Atualizar o status de um voo (ex: de `"programado"` para `"embarque"`).
* Atualizar o status de check-in do passageiro.
* Ao atribuir um portão a um voo, o campo `disponivel` do portão deve mudar para `false`.
* Quando o voo for concluído, o portão deve ser automaticamente liberado (`disponivel = true`).

### 4. Rota de Relatório JSON

Criação de uma rota que gere um relatório com:

* Todos os voos programados para o dia atual.
* Lista de passageiros por voo.
* Status de check-in de cada passageiro.
* Portão atribuído ao voo.

---

## 📅 Informações da Atividade

* **Curso**: Ciência da Computação – 7º Período
* **Disciplina**: Sistemas Distribuídos
* **Professor**: Alexandre Carvalho Silva
