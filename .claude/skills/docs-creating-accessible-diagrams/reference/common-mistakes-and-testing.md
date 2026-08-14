# Accessible Diagrams — Common Mistakes and Testing Tools

## Mistake 1: Using Red-Green Combinations

❌ **Problem**: ~8% of males cannot distinguish red/green

✅ **Solution**: Use Orange and Teal from verified palette

## Mistake 2: Relying on Color Alone

❌ **Problem**: Color-blind users can't distinguish elements

✅ **Solution**: Add text labels, use different shapes, provide context

## Mistake 3: Using Yellow for Important Info

❌ **Problem**: Yellow invisible to tritanopia (blue-yellow blindness)

✅ **Solution**: Use Orange or Teal instead

## Mistake 4: No Contrast Verification

❌ **Problem**: Insufficient contrast causes readability issues

✅ **Solution**: Use verified palette (all colors tested for WCAG AA)

## Mistake 5: Using CSS Color Names

❌ **Problem**: Inconsistent across platforms

```css
fill: red; /* WRONG */
```

✅ **Solution**: Always use hex codes

```css
fill: #de8f05; /* CORRECT */
```

## Mistake 6: Not Testing Dark Mode

❌ **Problem**: Colors may not work in dark backgrounds

✅ **Solution**: Verified palette works in both light and dark modes

## Color Blindness Simulators

- **Coblis Simulator**: <https://www.color-blindness.com/coblis-color-blindness-simulator/>
  - Upload diagram, view with protanopia/deuteranopia/tritanopia
  - Free, web-based

- **Figma Color Blind Plugin**: <https://www.figma.com/community/plugin/733159460536249875/Color%20Blind>
  - Requires Figma account
  - All color blindness types

## Contrast Checkers

- **WebAIM Contrast Checker**: <https://webaim.org/resources/contrastchecker/>
  - Enter foreground/background colors
  - Get WCAG compliance status
  - Free, web-based
