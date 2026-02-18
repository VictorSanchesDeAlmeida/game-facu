# 🎮 Demon Hunter

Um jogo de plataforma 2D desenvolvido em Python com Pygame, onde você enfrenta demônios em um cenário sombrio e atmosférico.

## 📋 Sobre o Projeto

**Demon Hunter** é um jogo de ação e plataforma onde o jogador deve eliminar todos os demônios de cada nível usando armas de fogo enquanto navega por plataformas. O jogo apresenta mecânicas de combate, sistema de vida, inimigos com IA, e efeitos visuais elaborados.

### 🎯 Objetivo

Elimine todos os demônios do nível para alcançar a vitória! Cuidado com os ataques inimigos e use suas habilidades de plataforma para sobreviver.

## ✨ Características

### Mecânicas do Jogador
- **Movimentação**: Ande para esquerda/direita e pule pelas plataformas
- **Combate**: Atire em direção aos inimigos com sua arma
- **Sistema de Vida**: 5 HP com período de invencibilidade após dano
- **Animações**: Animações suaves de idle e caminhada
- **Efeito de Disparo**: Flash visual ao atirar

### Inimigos (Demônios)
- **IA Inteligente**: Sistema de estados (Patrulha → Perseguição → Ataque)
- **Detecção**: Persegue o jogador quando está próximo (200 pixels)
- **Combate Corpo a Corpo**: Ataque melée com alcance de 55 pixels
- **Patrulha**: Caminha em uma área definida quando não detecta o jogador
- **3 HP**: Cada demônio precisa de 3 hits para ser eliminado

### Sistema de Combate
- Balas causam 1 de dano por acerto
- Knockback ao receber dano
- Sistema de cooldown entre ataques
- Detecção de colisão precisa

### Efeitos Visuais
- **Parallax Scrolling**: Fundo em 4 camadas (montanhas, árvores, névoa, decorações)
- **Sistema de Partículas**: Efeitos atmosféricos de cinzas e celebração
- **Câmera Suave**: Segue o jogador com interpolação
- **Tela de Game Over Elaborada**: Com efeitos dramáticos e rachaduras
- **HUD Completo**: Vida, contador de inimigos, status da arma, mini-radar

## 🛠️ Tecnologias Utilizadas

- **Python 3**: Linguagem principal
- **Pygame**: Engine do jogo para renderização, sprites e física
- **JSON**: Configuração de animações
- **PyInstaller**: Empacotamento em executável standalone

## 📁 Estrutura do Projeto

```
game-facu/
├── src/
│   ├── main.py              # Ponto de entrada do jogo
│   ├── game.py              # Classe principal do jogo
│   ├── config.py            # Configurações globais
│   ├── entities/            # Jogador e inimigos
│   │   ├── Player.py
│   │   └── Demon.py
│   ├── scenes/              # Gerenciamento de cenas
│   │   ├── SceneManager.py
│   │   ├── MenuScene.py
│   │   ├── GameScene.py
│   │   └── VictoryScene.py
│   ├── levels/              # Níveis do jogo
│   │   └── Level_1.py
│   ├── hud/                 # Interface do usuário
│   │   └── HUD.py
│   ├── sprite/              # Sistema de animação
│   │   ├── Skeleton.py
│   │   ├── Demon.json
│   │   └── Player.json
│   └── utils/               # Utilitários
│       ├── Camera.py
│       └── Collision.py
├── assets/                  # Recursos visuais
│   ├── Player.png
│   ├── Demon.png
│   ├── grass_block.png
│   └── rocky_block.png
├── main.spec                # Configuração do PyInstaller
└── README.md
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/VictorSanchesDeAlmeida/game-facu.git
cd game-facu
```

2. Instale as dependências:
```bash
pip install pygame
```

### Executar o Jogo

```bash
python src/main.py
```

## 🎮 Controles

| Ação | Tecla |
|------|-------|
| **Mover para Esquerda** | ← (Seta Esquerda) ou A |
| **Mover para Direita** | → (Seta Direita) ou D |
| **Pular** | ↑ (Seta Cima) ou W |
| **Atirar** | Espaço |
| **Sair** | ESC (no menu) |

## 📦 Gerar Executável

Para criar um executável standalone do jogo:

1. Instale o PyInstaller:
```bash
pip install pyinstaller
```

2. Execute o PyInstaller com o arquivo spec:
```bash
pyinstaller main.spec
```

3. O executável será gerado em `dist/DemonHunter.exe` (Windows) ou `dist/DemonHunter` (Linux/Mac)

## 🎯 Especificações Técnicas

### Estatísticas do Jogo
- **Resolução**: 1024×768 pixels
- **FPS Alvo**: 60 FPS
- **Tamanho do Mapa**: 1984×768 pixels (31×12 grid de tiles 64×64)
- **Vida do Jogador**: 5 HP
- **Vida dos Demônios**: 3 HP cada
- **Inimigos por Nível**: 4 demônios
- **Alcance de Detecção**: 200 pixels
- **Alcance de Ataque**: 55 pixels
- **Duração da Invencibilidade**: 1 segundo (60 frames)
- **Cooldown de Ataque**: 1.5 segundos (90 frames)

### Arquitetura
- **Padrão de Design**: Sistema baseado em cenas
- **Física**: Gravidade e detecção de colisão customizada
- **Animação**: Sistema skeletal com configuração JSON
- **Câmera**: Sistema de seguimento suave com interpolação

## 🎨 Características Visuais

- **Parallax de 4 Camadas**: Criando profundidade e imersão
- **Sistema de Partículas**: Cinzas atmosféricas e efeitos de celebração
- **Animações Suaves**: Transições fluidas entre estados
- **HUD Informativo**: Vida, contador de inimigos e mini-radar
- **Tela de Game Over Dinâmica**: Com efeitos especiais e diálogo

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais.

## 👤 Autor

**Victor Sanches De Almeida**

---

*Desenvolvido com ❤️ usando Python e Pygame*
