import requests


r = requests.get(r'https://comtrade.un.org/api/get?r=40&token=K2fLb7Sc8KBGradNiBkbXH5J%2FZqjWgw7rOTFh30CuSLTk6EIDBUgFzMDBTXt%2FdQ0ZrREdP757T7Vt%2BfoFSNyOCmjua2zbq8A3hIydgZ8KG3UCX8H4DNArADwWikBDPPFBVkWJ%2FZayuGLjCZIydp7MLxcTZbB41pecp%2F%2Bcm%2FpEQc%3D')

print(r.content)