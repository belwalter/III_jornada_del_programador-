from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair, CryptoKeypair

# creamos conexion a bd
bdb = BigchainDB(
    'https://test.bigchaindb.com/',
    headers={'app_id': 'f8a94c8b',
             'app_key': '060442e2780d46a66bf9833ee8e2e567'})

# definimos el activo
data = {'data': {'moneda': 'dolares',
                 'cantidad': 100}}

# y metadata si necesitamos
metadata = {'extra': 'info extra'}

# generamos identidades criptograficas
alice, bob = generate_keypair(), generate_keypair()
walter = generate_keypair()

# La clave privada se usa para firmar transacciones
# La clave pública se usa para verificar que una transacción
# firmada fue efectivamente firmada por el que dice ser el firmante.
# print(walter.private_key)
# print(walter.public_key)

# creamos activo para transacción
activo_preparado_tx = bdb.transactions.prepare(
    operation='CREATE',
    signers=alice.public_key,
    asset=data,
    metadata=metadata)

# print(activo_preparado_tx)

# firmamos la transaccion
activo_firmado_tx = bdb.transactions.fulfill(
    activo_preparado_tx, private_keys=alice.private_key)

# print(activo_firmado_tx)

envio_tx = bdb.transactions.send_commit(activo_firmado_tx)

# print(envio_tx == activo_firmado_tx)
# print(activo_firmado_tx['id'])


id = activo_firmado_tx['id']
# "2fd11d36cfc2c11ff6ee2f0e295f4cf967e8af876d57f416b91c2bff7bbad360"
#block_height = bdb.blocks.get(txid=activo_firmado_tx['id'])

block_height = bdb.blocks.get(txid=id)
#print(block_height)
block = bdb.blocks.retrieve(str(block_height))
# print(block)

transaccion_tx = activo_firmado_tx
asset_id = transaccion_tx['id']

trasferencia_asset = {
    'id': asset_id,
}

# print(transaccion_tx)

indice_salida = 0
salida = transaccion_tx['outputs'][indice_salida]
transfrencia_entrada = {
    'fulfillment': salida['condition']['details'],
    'fulfills': {
        'output_index': indice_salida,
        'transaction_id': transaccion_tx['id']},
    'owners_before': salida['public_keys'],
    }

print(transfrencia_entrada)

transferencia_preparada_tx = bdb.transactions.prepare(
    operation='TRANSFER',
    asset=trasferencia_asset,
    inputs=transfrencia_entrada,
    recipients=bob.public_key,
    )

# print(transaccion_tx)

transferencia_firmada = bdb.transactions.fulfill(
    transferencia_preparada_tx,
    private_keys=walter.private_key,
    )

# print(transferencia_firmada)

transferencia_enviada = bdb.transactions.send_commit(transferencia_firmada)

# print(transferencia_enviada == transferencia_firmada)

print(transferencia_firmada['outputs'][0]['public_keys'][0] == walter.public_key)

print(transferencia_firmada['inputs'][0]['owners_before'][0] == alice.public_key)
