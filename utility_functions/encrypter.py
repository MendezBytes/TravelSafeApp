from Cryptodome.Cipher import AES
from Cryptodome import Random

secret_key = b'4nf7mamc83nashn3'
def encode_license_num(driver_id,license_plate):
    license_plate = str(driver_id)+"_"+str(license_plate).upper()
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(secret_key, AES.MODE_CFB,iv)
    msg = iv + cipher.encrypt(str.encode(license_plate))
    return msg.hex()

def decode_license_num(encrypted_string):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(secret_key, AES.MODE_CFB, iv)
    decoded_string = cipher.decrypt(bytes.fromhex(encrypted_string))[len(iv):]
    driver_id,licence_plate = decoded_string.decode("utf-8").split("_")
    return decoded_string


# if __name__ == "__main__":
#     code=encode_license_num(1,"Pch4321",secret_key)
#     decode_license_num(code,secret_key)
