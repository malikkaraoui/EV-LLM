# E012 -- circuits rendus (MDL-minimaux)

## X1 graine 1 -- preuve FAUX

```
sortie = carre(-1/2 + -2/5*x1 + 7/5*x0)
```

## X1 graine 2 -- preuve FAUX

```
sortie = carre(1/2 + -7/5*x1 + 2/5*x0)
```

## X1 graine 3 -- preuve FAUX

```
sortie = carre(1/2 + 2/5*x1 + -7/5*x0)
```

## X1 graine 4 -- preuve FAUX

```
sortie = carre(1/2 + 2/5*x0 + -7/5*x1)
```

## X1 graine 5 -- preuve FAUX

```
sortie = carre(-3/5 + -1/3*x1 + 3/2*x0)
```

## X2-100 graine 1 -- preuve FAUX

```
sortie = floor(1*x0 + 1*x1 + 1/10*sortie(t-1))
```

## X2-100 graine 2 -- preuve PROUVE

```
h1 = id(-1/5*x1 + -1/5*x0 + -1/3*h2(t-1))
h2 = floor(-1/2*h1)
sortie = relu(1*x0 + 1*x1 + -10*h2 + 1*h2(t-1))
```

## X2-100 graine 3 -- preuve PROUVE

```
h1 = floor(1/10*x1 + 1/6*h1(t-1) + 1/10*x0)
sortie = relu(1*x1 + 1*x0 + -10*h1 + 1*h1(t-1))
```

## X2-100 graine 4 -- preuve FAUX

```
sortie = floor(1*x1 + 1*x0 + 1/10*sortie(t-1))
```

## X2-100 graine 5 -- preuve FAUX

```
sortie = floor(1*x0 + 1*x1 + 1/10*sortie(t-1))
```

## X2-1000 graine 1 -- preuve NON_PROUVABLE

```
h1 = carre(-2/5 + 1/5*x1)
h2 = sig(1 + -1/2*x1)
h3 = marche(-9/7 + 1/2*x0 + -5*h2 + 1/2*h3(t-1) + 1/2*h1)
h4 = floor(2*h3)
sortie = id(1*x0 + 1*x1 + 1*h3(t-1) + -4*h3 + -3*h4)
```

## X2-1000 graine 2 -- preuve NON_PROUVABLE

```
h1 = id(1/6*x0 + -1/10*x1)
h2 = floor(1*x1 + 11/9*h5(t-1))
h3 = relu(2*h5(t-1))
h4 = sig(1/2*h1 + 1/3*h3)
h5 = floor(1/7*x1 + 1/2*h1 + 1/3*h4)
sortie = id(1*x0 + 1*h2 + -10*h5)
```

## X2-1000 graine 3 -- preuve PROUVE

```
h1 = floor(-1/2 + 1/2*x1 + -1/2*x0 + -1/2*h2(t-1))
h2 = floor(1/3 + 1/9*x1 + -1/9*h1)
sortie = floor(1*x1 + 1*x0 + -10*h2 + 1*h2(t-1))
```

## X2-1000 graine 4 -- preuve FAUX

```
sortie = floor(1*x1 + 1*x0 + 1/10*sortie(t-1))
```

## X2-1000 graine 5 -- preuve PROUVE

```
h1 = marche(-9 + 1*x1 + 1*x0 + 1*h1(t-1))
sortie = id(1*x1 + 1*x0 + -10*h1 + 1*h1(t-1))
```

## X3 graine 1 -- preuve SANS_OBJET

```
h1 = id(1*x3 + -4/7*h1(t-1))
sortie = carre(1/2 + -1*h1 + -3*h1(t-1))
```

## X3 graine 2 -- preuve SANS_OBJET

```
h1 = floor(-5*x3 + -2/3*h1(t-1) + -2*x1 + 1/2*x2)
sortie = carre(1/3 + 1/2*h1(t-1) + 5*x2)
```

## X3 graine 3 -- preuve SANS_OBJET

```
h1 = tanh(1*sortie(t-1))
h2 = carre(-1/10 + 5*x3 + -2*h1(t-1))
sortie = relu(1/7*h2(t-1) + 2*x2)
```

## X3 graine 4 -- preuve SANS_OBJET

```
h1 = tanh(1/6 + 1*x3 + -1/2*x2 + -1/5*sortie(t-1))
sortie = carre(-1/2 + -3*h1(t-1))
```

## X3 graine 5 -- preuve SANS_OBJET

```
h1 = tanh(-2*x3)
sortie = carre(1/3 + 2*h1(t-1))
```
