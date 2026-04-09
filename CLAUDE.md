# Site Dra. Thielen Szczypkowski

## Estrutura
- HTML estático puro — sem build, sem framework
- CSS inline `<style>` em cada página para estilos específicos, CSS global em `css/style.css`
- JS compartilhado em `js/main.js`
- Assets em `assets/` — logo em `assets/logo-original.png`, favicon em `assets/favicon.png`
- Blog em subpasta `blog/` — paths de assets usam `../assets/`

## Seletores críticos
- A seção hero tem `id="main"` (não `id="hero"`) — CSS deve usar `#main`
- Header transparente no topo, `.scrolled` adicionado via JS ao rolar > 60px
- Animações de entrada: `.fade-up`, `.fade-left`, `.fade-right`, `.scale-in` — ativadas por IntersectionObserver em `main.js`

## Padrões de CSS
- Variáveis de cor em `:root` no `style.css` — usar sempre `var(--bronze)`, `var(--cream-light)` etc.
- `--radius-lg: 32px` — padrão para fotos; fotos usam `border-radius: 6px 32px 6px 32px` (assimétrico)
- Sombras em fotos: usar `filter: drop-shadow()` (não `box-shadow`) quando o elemento tem `overflow: hidden`
- `box-shadow` só funciona visível em elementos sem `overflow: hidden` no mesmo elemento

## Layout hero
- Hero usa CSS Grid com `grid-template-columns: 1fr 1fr` diretamente no `#main`
- Coluna esquerda: `.container` com `grid-column:1`
- Coluna direita: `.hero-img-outer` com `grid-column:2` inline — resetar com `!important` no responsive
- Foto sangra do topo: `.hero-img-wrap` com `position: absolute; inset: 0`
- No mobile (≤1024px): `grid-template-columns: 1fr` e `grid-column: 1 !important` na foto

## Header nav
- Antes do scroll: links brancos (`rgba(255,255,255,0.9)`), hover em `var(--bronze-light)`
- Após `.scrolled`: links voltam a `var(--text-muted)`, hover em `var(--bronze)`
- Botão CTA `.nav-cta` mantém bronze em ambos os estados

## Gotchas
- `overflow: hidden` corta `box-shadow` — usar `filter: drop-shadow` nas fotos
- Atributos `style` inline com `grid-column:2` bloqueiam o responsive — sempre usar `!important` para sobrescrever
- Wave/onda no final da hero: seção não pode ter `overflow: hidden`, senão o SVG é cortado
- Footer usa `.logo` com texto — não atualizar junto com o header ao trocar logo
