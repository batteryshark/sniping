import requests
import sys
import time
from pushover import init, Client

URL = "https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.ma.json?vaccineinfo"


TARGET_CITIES = [
"ALLSTON",
"BEVERLY",
"BOSTON",
"BRIGHTON",
"BROOKLINE",
"CAMBRIDGE",
"CHELSEA",
"EAST BOSTON",
"LYNN",
"MALDEN",
"MEDFORD",
"REVERE",
"SAUGUS",
"SOMERVILLE",
"STONEHAM"
]

HEADERS = {
'accept': '*/*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9',
'cookie':"adh_ps_pickup=on; bbcart=on; sab_newfse=on; sab_displayads=on; flipp2=on; mc_rio_locator3=on; mc_videovisit=on; pivotal_forgot_password=off-p0; pivotal_sso=off-p0; ps=on; rxhp=on; rxhp-two-step=off-p0; rxm=on; rxm_phone_dob=on; sab_deals=on; s2c_akamaidigitizecoupon=on; s2c_digitizecoupon=on; s2c_herotimer=off-p0; s2c_prodshelf=on; s2c_persistEcCookie=on; s2c_smsenrollment=on; sftg=on; show_exception_status=on; _group1=quantum; gbi_visitorId=ckl48jdxe00013c7kxuki3pi2; pe=p1; acctdel_v1=on; adh_new_ps=on; adh_ps_refill=on; buynow=off; dashboard_v1=off; db-show-allrx=on; disable-app-dynamics=on; disable-sac=on; dpp_cdc=off; dpp_drug_dir=off; dpp_sft=off; getcust_elastic=on; echomeln6=off-p2; enable_imz=on; enable_imz_cvd=on; enable_imz_reschedule_instore=on; enable_imz_reschedule_clinic=off; gbi_cvs_coupons=true; ice-phr-offer=off; v3redirecton=false; mc_cloud_service=on; mc_hl7=on; mc_home_new=on; mc_ui_ssr=off-p0; memberlite=on; pauth_v1=on; pbmplaceorder=off; pbmrxhistory=on; refill_chkbox_remove=off-p0; rxdanshownba=off; rxdfixie=on; rxd_bnr=on; rxd_dot_bnr=on; rxdpromo=on; rxduan=on; rxlite=on; rxlitelob=off; rxm_demo_hide_LN=off; rxm_phdob_hide_LN=on; rxm_rx_challenge=off; s2c_beautyclub=off-p0; s2c_dmenrollment=off-p0; s2c_newcard=off-p0; s2c_papercoupon=on; s2c_rewardstrackerbctile=on; s2c_rewardstrackerbctenpercent=on; s2c_rewardstrackerqebtile=on; s2cHero_lean6=on; sft_mfr_new=on; v2-dash-redirection=on; AMCVS_06660D1556E030D17F000101%40AdobeOrg=1; CVPF=CT-2; aat1=off-p1; akavpau_vp_www_cvs_com_minuteclinic_covid19=1617601103~id=77db29080874d207f09efcf3d09bbe3e; akavpau_vp_www_cvs_com_vaccine_covid19=1617602823~id=1caf4b51e6ade1456073e321f17da95a; ak_bmsc=BB10E18AC15FB8A00B09DCD74B2CD73417C2BE85C70B00006D0B6B604B2D9711~plhuruZDVKp/PZh8Fj+Zkfy4bF/DPe4MV72VkM6/Bw1OLIS3vLePzTWdBCYa0IxC1iwKt3Mwd4aXRZz8B35h0Zxy+vtTumxjxpqeVjZWBLuuQfx9IRc2azJQGK13elKFlbu1eulMc3uAeN6k3uhvwOY41j0BxItyLdkItwAX2YyvqTFRAT6x5hAneuYLW8zKdPZPgO/CFsXJtxkXFkcP9Y30SIT2V7eERVlPVVFAfdJr8=; bm_sz=00DF2491571EF55E3ABA42DAACA74587~YAAQhb7CFxUZnnR4AQAAlaMkogtX68luLrx2jWn8iMC+nJxaOuaWVrtKUtNPHNPrJFDG6B6GRvU5oaTVpPqzqArt99JHFcq4+zkZT4I8pX0XoUi7YIkSGOFhRDRGRtCkW1beuzx9DQSEnazGXHht0C2qO/8repAcdG0+CUckVLnQh3RIv/2V+MaRhHQp; _abck=1985680658043D9DF3685D79A923D411~0~YAAQhb7CFxYZnnR4AQAAlaMkogW92gzN2sbsIYzZgawQD/O5OkLsiToncHmfZ9TcWK5258f4FO2HxD75nT+Duq5/H3qABVK23eFjix1aX/Ml1w+trA2BblppctlhYujSfaGCxhusUauLhjIzawxJLvLIgurVZahqjHe/AgURyeQMF84A+LD4ZGwB6O6oLi9bVUR1A3mJ6yhzFSS6ocb311zKq6LJ+Kwd/aTilWa6DaMl5pjfcXvMPi2R/y7eYroQMhJpp3/9ReI9LMMlz3WJydNcEFgIU7eTyA03mAh4I82l/0eSDg9yHPNKEZ2hq1J5mig5TVbmIXg278qbquROHwgHoYKuF5HIKW4DJsMNN4TwSG1hcItr+76F3PQ+jPuqFiUMw5SSDf0FnC7l3t6mr+/igfao~-1~-1~-1; AMCV_06660D1556E030D17F000101%40AdobeOrg=-330454231%7CMCIDTS%7C18723%7CMCMID%7C35736489913889333449221173017962898125%7CMCAID%7CNONE%7CMCOPTOUT-1617635216s%7CNONE%7CvVersion%7C3.1.2; akavpau_vp_www_cvs_com_vaccine=1617628637~id=ee6fff81a25ab2d18221e479f01da573; akavpau_vp_www_cvs_com_pharmacy=1617628464~id=c9bfdf8a213314cdc61ad19e4ec912e4; current_page_name=cvs|dweb|content|coronavirus|PROMO: Coronavirus Resource Center: Testing and Vaccine Updates | CVS Pharmacy; previous_page_name=; previous_page_url=https://www.cvs.com/content/coronavirus?icid=rx-home-hero1-COVAX; gbi_sessionId=ckn4lz3wo00003cempe0tmex5; favorite_store=17807/42.361000/-71.062600/BOSTON/MA; utag_main=v_id:017797c9a7020017f5243d3b726103073003106b00fb8$_sn:5$_ss:0$_st:1617629852139$_pn:6%3Bexp-session$ses_id:1617628016188%3Bexp-session; akavpau_www_cvs_com_general=1617628472~id=b59261eaee4e33a72370d66fc057139d; bm_sv=D565A7E306E32CE3FFE783991F8367CA~+ItSyL6y5Yu0S9U5wW7IelOEAupKzWIY8vw7cYH9jxZbA/eY3SS0aE5siEGaL+UO2fKVz0DrTfS11JOVCs0OKXt8coQFNcBwNFqn0KQAjQVMrkoW1H5E+ziMxoFbrC5r6d7qUjk0YY+ace/SKaQ43A==",
'referer': 'https://www.cvs.com/immunizations/covid-19-vaccine?icid=coronavirus-lp-nav-vaccine',
'sec-ch-ua': "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"",
'sec-ch-ua-mobile': '?0',
'sec-fetch-dest': 'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-origin',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
}


def check_dates():
    init("CLIENT_ID")
    client = Client("API_KEY")
    while 1:
        r = requests.get(URL,headers=HEADERS)
        if r.status_code != 200:
            print(f"Error Code: {r.status_code}")
            sys.exit(-1)
        data = r.json()
        cities = data["responsePayloadData"]["data"]["MA"]
        for entry in cities:
            if entry['city'] in TARGET_CITIES:
                if entry['status'] != "Fully Booked":
                    client.send_message(f"Vaccine At {entry['city']} {entry['status']}!", title="VaccineTime!")
        time.sleep(5)

if __name__ == "__main__":
    check_dates()
    
        
    
