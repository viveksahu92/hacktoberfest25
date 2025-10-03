# 🚀 Stack Invaders

Bem-vindo ao **Stack Invaders**, um shooter retrô inspirado em Space Invaders onde cada fase homenageia uma linguagem de programação. Derrote ondas temáticas, colete power-ups e encare chefes que disparam palavras-chave!

## 🎮 Começando
- **Requisitos:** Python 3.10+ e [Pygame](https://www.pygame.org/). Instale com:
  ```bash
  pip install pygame
  ```
- **Execute o jogo:**
  ```bash
  python main.py
  ```
- **Dica de áudio:** O jogo continua mesmo sem áudio caso o mixer falhe ao iniciar, mas para a experiência completa verifique se o som do sistema está disponível.

## 🕹️ Como Jogar
- **Mover:** `←/→` ou `A/D`
- **Atirar:** `ESPAÇO`
- **Pausar / Voltar:** `ESC`
- **Objetivo:** Limpe as ondas de inimigos para chamar o chefe da fase. Vença o chefe para avançar ao próximo cenário temático.

### ⭐ Power-Ups
- **Tiro Duplo:** Dispara um projétil adicional temporariamente.
- **Escudo:** Cria uma barreira que absorve um impacto.
- **Tempo Lento:** Reduz a velocidade das ameaças por alguns segundos.

### 🧠 Dicas
- Mantenha-se em movimento para escapar dos padrões em leque e espiral dos chefes.
- Sincronize os tiros quando as fileiras inimigas mudam de direção para causar mais dano.
- Observe os projéteis com palavras-chave—os especiais dos chefes são mais rápidos e perigosos.

## 🛠️ Adicionando Novas Features
### 🆕 Nova Fase
As fases ficam na lista `STAGES` em `main.py`. Duplique um bloco existente e ajuste:
1. `name`, `color` e a grade de inimigos (`enemy_rows`, `enemy_cols`).
2. Parâmetros de dificuldade (`enemy_speed`, `enemy_drop`, `enemy_shoot_chance`, `enemy_hp`, `player_projectile_speed`).
3. Definição do chefe (dicionário `boss`) com HP, padrões, especiais e sprite.
Lembre-se de colocar sprites ou ícones personalizados em `assets/`.

### 🎯 Comportamento Personalizado
- **Visuais dos inimigos:** Aponte `enemy_sprite` para uma imagem customizada dentro da fase.
- **Padrões do chefe:** Estenda `Boss.fire_pattern` para criar novos ataques. Adicione um novo ramo no método e inclua projéteis em `enemy_bullets`.

### 🧩 Novos Power-Ups
`Player.apply_power` administra os bônus. Acrescente novos casos e gere-os a partir de `PowerUp` ou da lógica de ondas para testar mecânicas como tiro rápido ou multiplicadores de pontos.

### 🗂️ Organização
- Guarde os arquivos em `assets/` para evitar erros de carregamento.
- Reaproveite `try_load_image` e `try_load_sound` para ter fallbacks quando um recurso não existir.

## 📦 Estrutura do Repositório
```
Stackinvaders/
├── assets/         # Sprites, áudio e efeitos sonoros
├── main.py         # Loop principal, entidades e lógica de fases
├── README_EN.md    # Guia em inglês
└── README_PT.md    # Guia em português
```

Bom jogo e boas gambiarras intergalácticas! 🚀
