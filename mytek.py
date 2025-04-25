def scrapper_mytek_filtré(marque=None, prix_min=None, prix_max=None, processeur=None):
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import pandas as pd
    import time
    
    marques_dict = {
    "HP": "6332",
    "DELL": "6528",
    "LENOVO": "6784",
    "ASUS": "6395",
    "GIGABYTE": "6644",
    "MSI": "6862",
}
    
    processeur_dict = {
        "Intel Core i3": "337",
        "Intel Core i5": "338",
        "Intel Core i7": "339",
        "Intel Core i9": "340"
    }


    base_url = "https://www.mytek.tn/informatique/ordinateurs-portables/pc-portable.html"
    produits = []

    url = f"{base_url}?product_list_order=price&product_list_dir=asc"

    if marque:
        marque_id = marques_dict.get(marque.upper())
    if marque_id:
        url += f"&manufacturer={marque_id}"
    if processeur:
        processeur_id = processeur_dict.get(processeur)
    if processeur_id:
        url += f"&processeur={processeur_id}"
    if prix_min is not None and prix_max is not None:
        url += f"&price={int(prix_min)}-{int(prix_max)}"
    elif prix_min is not None:
        url += f"&price={int(prix_min)}-"
    elif prix_max is not None:
        url += f"&price=0-{int(prix_max)}"

    print(f"[URL filtrée] {url}")

    driver = uc.Chrome()
    time.sleep(2)
    driver.get(url)
   
    try:
        while True:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-item-info"))
                )
            except:
                print("[FIN] Aucun produit trouvé.")
                break

            items = driver.find_elements(By.CSS_SELECTOR, ".product-item-info")
            if not items:
                print("[FIN] Aucun article à traiter.")
                break

            for item in items:
                try:
                    nom = item.find_element(By.CSS_SELECTOR, ".product.name a").text
                    lien = item.find_element(By.CSS_SELECTOR, ".product.name a").get_attribute("href")
                    image = item.find_element(By.CSS_SELECTOR, "img.product-image-photo").get_attribute("src")
                    prix_text = item.find_element(By.CSS_SELECTOR, ".price").text

                    prix_clean = (
                        prix_text.replace("DT", "")
                        .replace("\u202f", "")
                        .replace(",", ".")
                        .strip()
                    )
                    prix = float(prix_clean)

                    try:
                        dispo_text = item.find_element(By.CSS_SELECTOR, ".stock").text
                    except:
                        dispo_text = "Indisponible"

                    produits.append({
                        "Nom": nom,
                        "Prix": prix,
                        "Disponibilité": dispo_text,
                        "Image": image,
                        "Lien": lien,
                        "Source": "MyTek"
                    })

                except Exception as e:
                    print(f"[Erreur produit] {e}")
                    continue

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'a.action.next')
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
    df.to_csv("produits_mytek.csv", index=False)
    return df
