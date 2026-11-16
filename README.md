# BIOJOUD

Site vitrine BIOJOUD en français et en arabe. Dernière version publiée : 16.

## Contenu

- 23 produits uniques, avec 46 fiches détaillées et deux pages d’accueil.
- Étiquettes et PDF originaux, visuels des bidons et des sacs.
- Catalogue responsive : deux produits par ligne sur mobile.
- Contact WhatsApp : +212 775 809 540, avec ouverture et copie du numéro.
- Métadonnées SEO, données structurées, sitemap et robots.txt.

## Hébergement statique

Le site prêt à publier se trouve dans `dist/`. Aucun build ni serveur applicatif n’est nécessaire.

Pour Cloudflare Pages connecté à ce dépôt :

- Branche : `main`
- Framework : `None`
- Commande de build : vide
- Répertoire de sortie : `dist`

Pour une autre plateforme statique, publier tout le contenu de `dist/`, y compris `assets/`, `produits/` et `ar/`.

Les URL SEO pointent vers l’adresse actuellement publiée. Après raccordement d’un domaine définitif, mettre à jour `BASE` dans `build_brand.py`, puis régénérer les pages avant publication.

## Modifier et vérifier

Python 3.12 ou ultérieur :

```bash
python build_brand.py
python verify_site.py
```

Les données des produits se trouvent dans `dist/products.json` et `dist/products-ar.json`. Le contact est défini dans `contact-settings.json`. Le style et les interactions sont dans `dist/brand.css` et `dist/brand.js`.

`make_packshots.py` reconstruit les visuels à partir des étiquettes originales. Cette opération facultative nécessite Pillow et CairoSVG. Les visuels prêts à publier sont déjà inclus.

Le formulaire de demande prépare un e-mail dans la messagerie du visiteur. Aucun message n’est envoyé automatiquement.
