#!/usr/bin/env python3
"""
Check nephron.com/org URLs to see which ones are valid and archivable
"""

import requests
import time

# URLs from the homepage scan
urls = [
    "http://hh.nephron.com",
    "http://nephron.com/dmprvnt.html",
    "http://nephron.com/goldennephron.html",
    "http://nephron.com/htkw.html",
    "http://nephron.com/ifkf2002_pres.html",
    "http://nephron.com/ifkf_pres03.htm",
    "http://nephron.com/kidneydisease.html",
    "http://nephron.com/nephsites/aakp-ckd-screening",
    "http://nephron.com/nephsites/nic/bill_buttonhole",
    "http://nephron.com/nephsites/nic/doi",
    "http://nephron.com/nephsites/nic/form_recipes",
    "http://nephron.com/nephsites/nic/kidney_study",
    "http://nephron.com/nephsites/nic/life.html",
    "http://nephron.com/nephsites/nic/message_to_patients",
    "http://nephron.com/nephsites/nic/michener.html",
    "http://nephron.com/nephsites/nic/michenertribute.html",
    "http://nephron.com/nephsites/nic/oneyearlater.html",
    "http://nephron.com/nephsites/nic/rememberingKris",
    "http://nephron.com/nephsites/nic/sarcoma_story",
    "http://nephron.com/nephsites/nkfset09",
    "http://nephron.com/ubb/Forum1/HTML/000023.html",
    "http://nephron.com/ubb/Forum1/HTML/000055.html",
    "http://nephron.org/cci",
    "http://nephron.org/diseases_categories/hereditary_nephritis/alport_syndrome",
    "http://nephron.org/diseases_categories/hereditary_nephritis/aminoaciduria",
    "http://nephron.org/diseases_categories/hereditary_nephritis/cystinosis",
    "http://nephron.org/diseases_categories/hereditary_nephritis/cystinuria",
    "http://nephron.org/diseases_categories/hereditary_nephritis/fabry_disease",
    "http://nephron.org/diseases_categories/hereditary_nephritis/familial_hypophosphatemia",
    "http://nephron.org/diseases_categories/hereditary_nephritis/fanconi_syndrome",
    "http://nephron.org/diseases_categories/hereditary_nephritis/hartnups_disease",
    "http://nephron.org/diseases_categories/hereditary_nephritis/hyperoxaluria",
    "http://nephron.org/diseases_categories/hereditary_nephritis/nail_patella",
    "http://nephron.org/diseases_categories/hereditary_nephritis/oculocerebrorenal_syndrome",
    "http://nephron.org/diseases_categories/hereditary_nephritis/pseudohypoaldosteronism",
    "http://nephron.org/diseases_categories/hereditary_nephritis/renal_glycosuria",
    "http://nephron.org/diseases_categories/hereditary_nephritis/renal_tubular_transport_errors",
    "http://nephron.org/diseases_categories/hereditary_nephritis/section_description",
    "http://nephron.org/diseases_categories/hereditary_nephritis/vhl",
    "http://nephron.org/diseases_categories/interstitial_nephritis/allergic_nephropathies",
    "http://nephron.org/diseases_categories/interstitial_nephritis/balkan_nephropathy",
    "http://nephron.org/diseases_categories/interstitial_nephritis/chemotherapy",
    "http://nephron.org/diseases_categories/interstitial_nephritis/heavy_metals",
    "http://nephron.org/diseases_categories/interstitial_nephritis/myeloma_kidney",
    "http://nephron.org/diseases_categories/interstitial_nephritis/section_description",
    "http://nephron.org/diseases_categories/other_conditions/cortical_necrosis",
    "http://nephron.org/diseases_categories/other_conditions/diabetes_insipidus",
    "http://nephron.org/diseases_categories/other_conditions/renal_tuberculosis",
    "http://nephron.org/diseases_categories/other_conditions/section_description",
    "http://nephron.org/diseases_categories/primary_gn/fgs",
    "http://nephron.org/diseases_categories/primary_gn/membranoproliferative_gn",
    "http://nephron.org/diseases_categories/primary_gn/membranous_nephropathy",
    "http://nephron.org/diseases_categories/primary_gn/minimal_change_gn",
    "http://nephron.org/diseases_categories/rpgn/anti_gbm",
    "http://nephron.org/diseases_categories/rpgn/churg_strauss",
    "http://nephron.org/diseases_categories/rpgn/goodpasture_syndrome",
    "http://nephron.org/diseases_categories/rpgn/microscopic_variant_pan",
    "http://nephron.org/diseases_categories/rpgn/pauci_immune_glomerulonephritis",
    "http://nephron.org/diseases_categories/rpgn/polyarteritis_nodosa",
    "http://nephron.org/diseases_categories/rpgn/section_description",
    "http://nephron.org/diseases_categories/rpgn/wegeners",
    "http://nephron.org/diseases_categories/secondary_nephritis/aids_nephropathy",
    "http://nephron.org/diseases_categories/secondary_nephritis/amyloidosis",
    "http://nephron.org/diseases_categories/secondary_nephritis/diabetic-nephropathy",
    "http://nephron.org/diseases_categories/secondary_nephritis/glomerulonephritis_infectious",
    "http://nephron.org/diseases_categories/secondary_nephritis/hepatitis",
    "http://nephron.org/diseases_categories/secondary_nephritis/lupus_nephritis",
    "http://nephron.org/diseases_categories/secondary_nephritis/myeloma",
    "http://nephron.org/diseases_categories/secondary_nephritis/sarcoid",
    "http://nephron.org/diseases_categories/secondary_nephritis/scleroderma",
    "http://nephron.org/diseases_categories/syndromes/acid_base_disorders",
    "http://nephron.org/diseases_categories/syndromes/acute_kidney_failure",
    "http://nephron.org/diseases_categories/syndromes/albuminuria",
    "http://nephron.org/diseases_categories/syndromes/chronic_kidney_disease",
    "http://nephron.org/diseases_categories/syndromes/chronic_kidney_failure",
    "http://nephron.org/diseases_categories/syndromes/cystic_kidneys",
    "http://nephron.org/diseases_categories/syndromes/electrolytes",
    "http://nephron.org/diseases_categories/syndromes/fanconi_syndrome",
    "http://nephron.org/diseases_categories/syndromes/glomerulonephropathies",
    "http://nephron.org/diseases_categories/syndromes/hematuria",
    "http://nephron.org/diseases_categories/syndromes/hemolytic_uremic_syndrome",
    "http://nephron.org/diseases_categories/syndromes/hepatorenal_syndrome",
    "http://nephron.org/diseases_categories/syndromes/hydronephrosis",
    "http://nephron.org/diseases_categories/syndromes/hypertension",
    "http://nephron.org/diseases_categories/syndromes/kidney_neoplasms",
    "http://nephron.org/diseases_categories/syndromes/kidney_stones",
    "http://nephron.org/diseases_categories/syndromes/mbd",
    "http://nephron.org/diseases_categories/syndromes/nephritis",
    "http://nephron.org/diseases_categories/syndromes/papillary_necrosis",
    "http://nephron.org/diseases_categories/syndromes/prostate_disorders",
    "http://nephron.org/diseases_categories/syndromes/proteinuria",
    "http://nephron.org/diseases_categories/syndromes/pyelonephritis",
    "http://nephron.org/diseases_categories/syndromes/renal_artery_obstruction",
    "http://nephron.org/diseases_categories/syndromes/renalvasculardisease",
    "http://nephron.org/diseases_categories/syndromes/rta",
    "http://nephron.org/diseases_categories/syndromes/section_description",
    "http://nephron.org/diseases_categories/syndromes/transplantation",
    "http://nephron.org/diseases_categories/syndromes/uremia",
    "http://nephron.org/diseases_categories/syndromes/vasculitis",
    "http://nephron.org/diseases_categories/syndromes/zellweger syndrome",
    "http://nephron.org/nephsites/journal_articles",
    "http://nephron.org/nephsites/journals/index_html",
    "http://nephron.org/nephsites/nic/access_schon_06907",
    "http://nephron.org/nephsites/nic/administrator",
    "http://nephron.org/nephsites/nic/clinical_trials",
    "http://nephron.org/nephsites/nic/disasters",
    "http://nephron.org/nephsites/nic/fadem",
    "http://nephron.org/nephsites/nic/guestbook_form",
    "http://nephron.org/nephsites/nic/headlines",
    "http://nephron.org/nephsites/nic/tours_angioaccess2010",
    "http://nephron.org/php/CFC.htm",
    "http://nephron.org/php/Meaningful_Use.htm",
    "http://www.nephron.org/issues",
    "http://www.nephron.org/issues/practice%20management/av/rpa_05",
    "http://www.nephron.org/nephsites/disaster_page",
    "http://www.nephron.org/nephsites/journal_articles",
    "http://www.nephron.org/nephsites/nic/dorsum",
    "http://www.nephron.org/nephsites/nic/fadem",
    "http://www.nephron.org/nephsites/nic/patents",
    "http://www.nephron.org/nephsites/nic/saving_veins.html",
    "http://www.nephron.org/nephsites/nic/self_cannulation.htm",
    "http://www.nephron.org/nephsites/nic/service.html",
    "http://www.nephron.org/nephsites/nic/tifrecipes",
    "http://www.nephron.org/nephsites/nic/zen_weintraub.html",
]

# Already archived
archived = [
    "http://www.nephron.org/nephsites/adp/",
    "http://www.nephron.org/nephsites/lundin",
    "http://www.nephron.org/nephsites/nic/shaldon_40yrs/",
]

valid_urls = []
error_urls = []
redirect_urls = []

print(f"Checking {len(urls)} URLs...\n")

for url in urls:
    try:
        # Don't follow redirects initially to detect them
        response = requests.head(url, timeout=5, allow_redirects=False)
        status = response.status_code
        
        # Check for redirects (301, 302, 303, 307, 308)
        if status in [301, 302, 303, 307, 308]:
            print(f"↪ {url} (Redirect: {status})")
            redirect_urls.append((url, status))
        elif status == 200:
            # Check if it's actual HTML content (not JavaScript redirect)
            try:
                full_response = requests.get(url, timeout=5)
                content = full_response.text.lower()
                
                # Check for JavaScript redirects
                if 'window.location' in content or 'document.location' in content or '<meta http-equiv="refresh"' in content:
                    print(f"⟳ {url} (JS Redirect)")
                    redirect_urls.append((url, "JS Redirect"))
                else:
                    print(f"✓ {url}")
                    valid_urls.append(url)
            except:
                print(f"✓ {url} (assuming valid)")
                valid_urls.append(url)
        else:
            print(f"✗ {url} (Status: {status})")
            error_urls.append((url, status))
            
    except requests.exceptions.RequestException as e:
        print(f"✗ {url} (Error: {str(e)[:50]})")
        error_urls.append((url, "Error"))
    
    time.sleep(0.3)  # Be nice to the server

print(f"\n{'='*60}")
print(f"SUMMARY:")
print(f"Valid URLs: {len(valid_urls)}")
print(f"Redirect URLs: {len(redirect_urls)}")
print(f"Error URLs: {len(error_urls)}")
print(f"{'='*60}\n")

print("VALID ARCHIVABLE URLs:")
for url in valid_urls:
    print(f"  {url}")
