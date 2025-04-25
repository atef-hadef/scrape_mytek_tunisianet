def scrapper_tunisianet(marque=None, prix_min=None, prix_max=None, processeur=None):
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import pandas as pd
    import time
    
    base_url = "https://www.tunisianet.com.tn/301-pc-portable-tunisie"
    url = base_url + "?"

    if marque:
        url += f"fabricants={marque.lower()}&"
    if processeur:
        processeur_formatté = processeur.replace(" ", "-")
        url += f"processeur={processeur_formatté.lower()}&"
    if prix_min is not None and prix_max is not None:
        url += f"&prix={int(prix_min)}-{int(prix_max)}"
    elif prix_min is not None:
        url += f"&prix={int(prix_min)}-"
    elif prix_max is not None:
        url += f"&prix=0-{int(prix_max)}"

    print(f"[URL] {url}")
    options = uc.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(options=options)
    time.sleep(3)
    driver.get(url)
        
    produits = []

    try:
        while True:
            items = driver.find_elements(By.CSS_SELECTOR, '.product-miniature')
            if not items:
                    print("[FIN] Aucun article à traiter.")
                    break
            for item in items:
                try:
                    nom_elem = item.find_element(By.CSS_SELECTOR, '.h3.product-title')
                    nom = nom_elem.text.strip()
                    print(nom)
                    lien_elem = nom_elem.find_element(By.TAG_NAME, 'a')
                    lien = lien_elem.get_attribute('href')

                    print(lien)
                    try:
                        image = item.find_elements(By.CSS_SELECTOR, ".center-block.img-responsive")
                        if image:

                            images = image[0].get_attribute("src")
                            print("Image URL:", images)
                        else:
                            print("Aucune image trouvée pour ce produit.")
                    except Exception as e:
                        print(f"[!] Erreur sur un produit : {e}")

                    try:
                        prix_text = item.find_element(By.CSS_SELECTOR, '.wb-action-block .product-price-and-shipping span.price').text
                        prix_clean = (
                            prix_text.replace("DT", "")
                                    .replace(' ', '')
                                    .replace("\xa0", "")
                                    .replace("\u202f", "")
                                    .replace(",", ".")
                                    .strip()
                        )
                        if not prix_clean:
                            raise ValueError("Prix vide")
                        prix = float(prix_clean)
                        print(prix)
                    except Exception as e:
                        print(f"[!] Prix non valide : {e}")
                        continue


                    
                    try:
                        dispo_element = item.find_element(By.CSS_SELECTOR, '.wb-action-block #stock_availability span')
                        dispo_text = dispo_element.text.strip()
                        print("Disponibilité :", dispo_text)
                    except Exception as e:
                        dispo_text = "Indisponible"
                        print(f"[!] Erreur disponibilité : {e}")



                    
                    produits.append({
                        "Nom": nom,
                        "Prix": prix,
                        "Disponibilité": dispo_text,
                        "Image": images,
                        "Lien": lien,
                        "Source": "Tunisianet"
                    })

                except Exception as e:
                    print(f"Erreur carte : {e}")
                    continue

                
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'a.next.js-search-link')
                if 'disabled' in next_button.get_attribute("class"):
                    print("[FIN] Plus de pages.")
                    break
                else:
                    print("[PAGE SUIVANTE]")
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(2)  
            except Exception as e:
                print(f"[Erreur bouton suivant] {e}")
                break

    finally:
        driver.quit()

    df = pd.DataFrame(produits)
    df.to_csv("produit_tunisianet.csv", index=False)
    return df

