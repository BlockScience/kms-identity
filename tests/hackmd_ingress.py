import api
from rid_lib.means import *

urls = [
  "https://hackmd.io/_t0p8m4KTQKT0NxeYOuB4w",
  "https://hackmd.io/mAsDQeRZRIG7hY4QejQofQ",
  "https://hackmd.io/@3goKpZI6Q9CZ9s6G9bqtqA/Sy1zsh0jL",
  "https://hackmd.io/@6CeZ7pUbT1mJFIkrbPJq-g/Sk2oNucDF",
  "https://hackmd.io/@benschza/rJpLRmfzu",
  "https://hackmd.io/@bsci-filecoin/ByzCOO2vD",
  "https://hackmd.io/@bsci-filecoin/H1hol_LhD",
  "https://hackmd.io/@bsci-gitcoin/BJcVklj5w",
  "https://hackmd.io/@bsci-gitcoin/BkA8tOi4O",
  "https://hackmd.io/@bsci-gitcoin/Bkkr4CQbO",
  "https://hackmd.io/@bsci-gitcoin/BkZ31HYxt",
  "https://hackmd.io/@bsci-gitcoin/HJxPEIMAv",
  "https://hackmd.io/@bsci-gitcoin/rJJNJiYgt",
  "https://hackmd.io/@bsci-gitcoin/ryeeD-7-d",
  "https://hackmd.io/@bsci-gitcoin/ryf6gaJEt",
  "https://hackmd.io/@bsci-gitcoin/S1iSyNN6Y",
  "https://hackmd.io/@bsci-gitcoin/SJcPqmKet",
  "https://hackmd.io/@bsci-gitcoin/SkYqV20UY",
  "https://hackmd.io/@bsci-gitcoin/SyNw03cx_",
  "https://hackmd.io/@bsci-holo/H1xx_Mpkc",
  "https://hackmd.io/@bsci-holo/Hyf9ko7k9",
  "https://hackmd.io/@bsci-holo/SyW9nG9XF",
  "https://hackmd.io/@bsci-rai/H1cmeYXTO",
  "https://hackmd.io/@bsci-rai/r1sT9Ma5d",
  "https://hackmd.io/@cag/SytDBGieY/",
  "https://hackmd.io/@danlessa/BJAiXB4w_",
  "https://hackmd.io/@danlessa/H1h5inmPw",
  "https://hackmd.io/@danlessa/SJm8sSBtO",
  "https://hackmd.io/@Jiajia20/HkRBKyuDu",
  "https://hackmd.io/@Jiajia20/rJbrU8eVO",
  "https://hackmd.io/@Jiajia20/rJpnRojdd",
  "https://hackmd.io/@Jiajia20/ryOGXi1mt",
  "https://hackmd.io/@Jiajia20/S1-ColL9u",
  "https://hackmd.io/@jshorish/B1ZnqKXKO",
  "https://hackmd.io/@jshorish/BkWnHl4D_",
  "https://hackmd.io/@jshorish/Byh2BMsEF",
  "https://hackmd.io/@jshorish/ByQvu2uN_",
  "https://hackmd.io/@jshorish/H19OZgwB_",
  "https://hackmd.io/@jshorish/H1BeoxOeu",
  "https://hackmd.io/@jshorish/H1nn-JHYY",
  "https://hackmd.io/@jshorish/HJfAjcVhP",
  "https://hackmd.io/@jshorish/HJlPLR06t",
  "https://hackmd.io/@jshorish/HJp12-71d",
  "https://hackmd.io/@jshorish/HJvW3siKu",
  "https://hackmd.io/@jshorish/Hk9dGq0X_",
  "https://hackmd.io/@jshorish/Hkdj9NhRw",
  "https://hackmd.io/@jshorish/Hy_TAieoF",
  "https://hackmd.io/@jshorish/HyYFSb-zu",
  "https://hackmd.io/@jshorish/r1gen2v7u",
  "https://hackmd.io/@jshorish/r1hLFcojw",
  "https://hackmd.io/@jshorish/r1OUgvUhD",
  "https://hackmd.io/@jshorish/rJNQQOitu",
  "https://hackmd.io/@jshorish/rkBg4sFAP",
  "https://hackmd.io/@jshorish/rkiiaglCY",
  "https://hackmd.io/@jshorish/ryJwZmQ3Y",
  "https://hackmd.io/@jshorish/S1iYcQUzd",
  "https://hackmd.io/@jshorish/S1zDN2r2F",
  "https://hackmd.io/@jshorish/Sk2sOgyH_",
  "https://hackmd.io/@jshorish/Skgbvj1K_",
  "https://hackmd.io/@jshorish/SyVMbA2FO",
  "https://hackmd.io/@kZSUsYNVTTebIcR5BVH8ug/BkvwDfL6O",
  "https://hackmd.io/@markusbkoch/HkyM3Lylv",
  "https://hackmd.io/@mbarlin/HyO9eVyku",
  "https://hackmd.io/@OCPoXLLVQvyCK3HvlpBEXg/rkuuWa3o_",
  "https://hackmd.io/@OCPoXLLVQvyCK3HvlpBEXg/ryEhFaatP",
  "https://hackmd.io/@OCPoXLLVQvyCK3HvlpBEXg/S1X824Chv",
  "https://hackmd.io/@poliwop/ryeUYgVn_",
  "https://hackmd.io/@RoboTeddy/SkFEYwptd",
  "https://hackmd.io/@rogervs/r1M6El7L_",
  "https://hackmd.io/@sissondf/ryu4S1yPY",
  "https://hackmd.io/@sissondf/SyaN1IZPK",
  "https://hackmd.io/0f6sEZNpQsSdJ7NhFmXDeA",
  "https://hackmd.io/0j3m0ymPQ_eRWF4eB_lY_w",
  "https://hackmd.io/0yoHKkEDTau9JEQRphQVQQ",
  "https://hackmd.io/1aUnx2YhTUmz8QYhG2A4PQ",
  "https://hackmd.io/2a0UGH21QPCge6D9nL4EyQ",
  "https://hackmd.io/2ertk4C0SByepteAnl-kFw",
  "https://hackmd.io/2hFUaRRiT72VzxaB8yWwEA",
  "https://hackmd.io/2uJfvgpFSdaOcZTw6R_QBQ",
  "https://hackmd.io/2ZNhSq0OTQmpr4rKTUnvmw",
  "https://hackmd.io/2zYJKXgMTA-CQJ17Crmfsw",
  "https://hackmd.io/3-yFv4ziQEys6JIkjDxgoA",
  "https://hackmd.io/3dGROn79TTOua-GV9mezsQ",
  "https://hackmd.io/4vkjV7vFS6GE0hUCoOJxAQ",
  "https://hackmd.io/52HOmYRNQfu0ln_W_3kcWw",
  "https://hackmd.io/5HAquZAARHShY6bISNx4-A",
  "https://hackmd.io/5jhFIVtARFK0WLESFXDzwQ",
  "https://hackmd.io/6bUzwavmRx6VpidHEvOhYw",
  "https://hackmd.io/6Mp5cxw6R8qTNhXKs9yiFQ",
  "https://hackmd.io/6R5-eZkySR-ujX6Ex49lYw",
  "https://hackmd.io/6x_r9ZU4QL6otIjnapkGkg",
  "https://hackmd.io/77NDwQ5tSLOG3hSzTw5W-Q",
  "https://hackmd.io/78w9XuMUQa21n1OJBSWrSA",
  "https://hackmd.io/7HYPPp7zQcShQLrKQ2KOxQ",
  "https://hackmd.io/7Z2e-Is7Toi-5SaRl4K3tA",
  "https://hackmd.io/9Iqz7nr5TDu00TUkTSOXwg",
  "https://hackmd.io/ABJRYVDlQ8iiz7O9VSIIDg",
  "https://hackmd.io/aIVEsHtHRK-QweOfOeBcdA",
  "https://hackmd.io/akxfOvWqTyGP6X8ie_Z8qA",
  "https://hackmd.io/ALlC-EAMSmm12S3033p0hQ",
  "https://hackmd.io/AoEnu22BTnyjS4GgkA7SBA",
  "https://hackmd.io/bdtW0ngxReqALhc1NkOf8g",
  "https://hackmd.io/bSygNThgRYqC9eniRIJ3zQ",
  "https://hackmd.io/bz5YGjg_QLW0sq2exYQG4Q",
  "https://hackmd.io/Cap-LGObRk-_6QD-Cmc9KQ",
  "https://hackmd.io/ce5nqBDRSViPjZ3ElMGyGA",
  "https://hackmd.io/cFHYvP2QQ8eKIKTkEUiaVw",
  "https://hackmd.io/cFP24y0wRLe31hTO-s1bnw",
  "https://hackmd.io/chn_LzBiS3as7yh3R9l2HA",
  "https://hackmd.io/cjtb3in5QzW5rpUG1SNiDQ",
  "https://hackmd.io/crGYG06HRfqo3FsnInhrkg",
  "https://hackmd.io/CrXePg7wQa24mIUTr9Mr2A",
  "https://hackmd.io/dJ1xIPpzRqyTfiu4EbZkeg",
  "https://hackmd.io/dkoI-i-xQwm9AneTtroIxA",
  "https://hackmd.io/e2mZ9UT7QRGMh5tg6OCXfw",
  "https://hackmd.io/ENCor5FQRFerVvDOjh2LlQ",
  "https://hackmd.io/etX4myH2Tn-AVD0saRoGHA",
  "https://hackmd.io/FL8axXOyRlW-Be_dqIFCIQ",
  "https://hackmd.io/fnTas8ARR86Yj80ogjvpPw",
  "https://hackmd.io/FphHh83iRxyrLPy894E1Tw",
  "https://hackmd.io/FvRc-QdjQWafDIbHFNQJgw",
  "https://hackmd.io/G3I7LCtcQ8yqiPHRyDZ6qA",
  "https://hackmd.io/gqu8bqdZSqyD3BJzo5gCkA",
  "https://hackmd.io/hEEthMNbQ_mrQsVZX-f0Lg",
  "https://hackmd.io/HokDuV_ISD23xx-o3-Jsng",
  "https://hackmd.io/hOsM_SNTRxSF2rFXpLSwZg",
  "https://hackmd.io/hsN-E0LgRgy7Ax2p3Ny1VA",
  "https://hackmd.io/HuOL6n6YQJyFdK8ZILtmmg",
  "https://hackmd.io/hUz7OHV2REC_SMwkPsgleA",
  "https://hackmd.io/HXQ3yWfBQN6QGQX4cmOAxQ",
  "https://hackmd.io/hzvgC7-TQaqtxDY-HudABA",
  "https://hackmd.io/Ide2XdeGQ_mOiMWQqhU7pA",
  "https://hackmd.io/isdzhSLeSauzS5v6thhFcA",
  "https://hackmd.io/ItS5VRqfSk2-PWnvnGduCA",
  "https://hackmd.io/iUjSWXWqQsqZZzyGJZDRag",
  "https://hackmd.io/iv6D-kO6QpWxcBW0-SXqWA",
  "https://hackmd.io/J1jc1-XUSUanKVzyEQL1Hg",
  "https://hackmd.io/J2-_mLtxSmKVaX3h9Tu9pA",
  "https://hackmd.io/j4wvYvqwT3GTtRW7yP7qEA",
  "https://hackmd.io/J6bgkZ3dQdmzyejYZgy8BQ",
  "https://hackmd.io/JliNBSTmQ-qPpo1R7ckarA",
  "https://hackmd.io/jSoOew33SxqwEDOR15gjhw",
  "https://hackmd.io/jWlia12DQ6SBLpKGLP9_-g",
  "https://hackmd.io/k0LR5cLRRQSUR9dzemfVBA",
  "https://hackmd.io/k71ZUSTxQVKGqOcvR6OXnw",
  "https://hackmd.io/KC8b0Q9dSzOKapRa93pHJA",
  "https://hackmd.io/kobi1Sr8RHuXC3F-KFl-_Q",
  "https://hackmd.io/kQjeYPUCQgmkY6GivmUynA",
  "https://hackmd.io/lb6MSl-jQz68r64Nh74GMg",
  "https://hackmd.io/lFi-00YWShqpjKgJu7Dc8A",
  "https://hackmd.io/lKL8wLXeQ4uhx_YEQ-j6zg",
  "https://hackmd.io/lXBFUoPiS9KoYxzfXKe9Ag",
  "https://hackmd.io/M7OeWimITKGVxBDHGQa6gQ",
  "https://hackmd.io/m9Ue_fltS9Oegja4F_dGtw",
  "https://hackmd.io/MU7mVUFoRsqIRHfnWXqeKA",
  "https://hackmd.io/n0Fm0-n7RiahTX2H4Ssa7Q",
  "https://hackmd.io/n1m7oRTFSViO5irJr96c_g",
  "https://hackmd.io/N1VkRma-T5G4fr1jR4pnLg",
  "https://hackmd.io/Na90sUp-T7Ksr20fb0S6UQ",
  "https://hackmd.io/nKt3o_FATxGcW_bXOSPj1Q",
  "https://hackmd.io/Nl1Zv746R-ODfrxwio5x7Q",
  "https://hackmd.io/noaQyFQJRQ2HdbD6EAZYrg",
  "https://hackmd.io/Npb5hM2DS5mK5H30DXNcpg",
  "https://hackmd.io/NXJNI2YVQziB3STBNH2Wjw",
  "https://hackmd.io/owviUNfeRkmSlgtJQcaQFg",
  "https://hackmd.io/OxX9ECXgTeuEuYzDo_GXqA",
  "https://hackmd.io/p_EwqgssST-Z6qJ98O4fyw",
  "https://hackmd.io/pDc6UM9tSiCZUjoEv7GMNQ",
  "https://hackmd.io/Poli5rQdT6WzutTjC0fNZw",
  "https://hackmd.io/PSa3CAAZS9mq090MqJB9YA",
  "https://hackmd.io/q_41NH2WSEmyxXzBhqeUUA",
  "https://hackmd.io/Q23FjbZZTvqLZwA0nYyJBQ",
  "https://hackmd.io/Qb8lEA4vRk-6qJG827bgDg",
  "https://hackmd.io/QCCJWZE0Ru27X_GRk6UKjQ",
  "https://hackmd.io/QJyDQ9M5Qh2o_PtJ2n_qZA",
  "https://hackmd.io/QKccU_ZPTUejzC-a3_A7Eg",
  "https://hackmd.io/QQ0fBz6kTPmJ0c_oM_y-Nw",
  "https://hackmd.io/QqwxjpAdSl2Bsf4vrBXQKQ",
  "https://hackmd.io/R0Xy8MetS5ytkekrGKgCFw",
  "https://hackmd.io/rl02mJcMSgSJ781QmKLKkQ",
  "https://hackmd.io/RROs81VaQbmdJHgN--tpsg",
  "https://hackmd.io/S_Pn8I3cSHuDbmv4Fc0inw",
  "https://hackmd.io/s/HkOrsOQ6Q",
  "https://hackmd.io/s/rkVcEVlj7",
  "https://hackmd.io/SBFzYzkaRvK3eUYThKD3Ww",
  "https://hackmd.io/SgaVxADYRveZdZwsG2M6GA",
  "https://hackmd.io/sHhp-CoUTf2SeZy6vJ8EcA",
  "https://hackmd.io/slh0z1pNRkuiAmPsn6mZPA",
  "https://hackmd.io/smLQ-QXdTse2dz1c6-Z85w",
  "https://hackmd.io/team/bsci-gitcoin",
  "https://hackmd.io/team/gds-maid-research",
  "https://hackmd.io/tfQQnZNPTGGHDTmD9uk1Yg",
  "https://hackmd.io/TndzPkLtRN63pik7qcPqRA",
  "https://hackmd.io/tvdQOIbjR-Www4sAGCMAhg",
  "https://hackmd.io/uS8U9NkZSwyHc97X6Gwn8A",
  "https://hackmd.io/uvbeYhNnTwunM0Z6CHGHOw",
  "https://hackmd.io/UwAaNMPxRhyn_cXM1h-25Q",
  "https://hackmd.io/V29PtP5CTd-h_1YX8Gp3JA",
  "https://hackmd.io/VAtUkwGmRyONRWm-2IlXeg",
  "https://hackmd.io/vkWRjXerQzmDXpOQCTKwdg",
  "https://hackmd.io/w-vfdZIMTDKwdEupeS3qxQ",
  "https://hackmd.io/WBdL5DevQTePvGqLGUsRpw",
  "https://hackmd.io/winlqVbyT0adfpN-QKuD6A",
  "https://hackmd.io/X-hKchuJSMCauaFkzcYHGA",
  "https://hackmd.io/X9sK2r2DTLexvIDyclfw5Q",
  "https://hackmd.io/XbQmM7J4SnSZc2EMsAeokg",
  "https://hackmd.io/XdCMH5DtRHyPNLCGDFZ-oQ",
  "https://hackmd.io/xfaw1LXvQzCfr8yf9gjgng",
  "https://hackmd.io/xhBDRc_LSRGrz6DRLTHvIg",
  "https://hackmd.io/XIrYcASUSqe42a4anBDmWQ",
  "https://hackmd.io/XVaejEw-QaCghV1Tkv3eVQ",
  "https://hackmd.io/y302YrhfRXm64j_51fbEGA",
  "https://hackmd.io/ynez1CzJS6KPRByPzCwhfA",
  "https://hackmd.io/yQQ4lo9VT9y6nMs-OiiJHg",
  "https://hackmd.io/YS2YrW1rTGSstFGl2nT1eg",
  "https://hackmd.io/yz23fxgtRvOawlQcp17Nzw",
  "https://hackmd.io/Z_7pw2c0RcWuDx4J-pyLtQ",
  "https://hackmd.io/zgoLdIHlS7SK3hAkxCrP3g",
  "https://hackmd.io/zqSkxhNvT-Gr9OSg6_ykSQ",
]

api.database.drop()

for url in urls:
    obj = URL(url).transform(means="hackmd")
    obj.observe()

    print(obj)