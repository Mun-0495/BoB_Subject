import hashlib
import datetime
import json
import random
import nodelib
import viewlib

nodes = []
nodeCount = 10
limit = 2000
view = viewlib.View()
reward = 50

def get_gen_block():
    block = {
        'ver': 1,
        'prev_hash': '',
        'mrkl_root': '',
        'time': datetime.datetime.now().timestamp(),
        'difficulty': 'f' * 512,
        'nonce': 0,
        'transactions': []
    }

    difficulty = int(block['difficulty'], 16)

    while True:
        block['nonce'] += 1
        block_hash = hashlib.sha256(json.dumps(block).encode()).hexdigest()
        if int(block_hash, 16) < difficulty:
            break

    return block


def init():
    gen_block = get_gen_block()
    for i in range(nodeCount):
        node = nodelib.Miner()
        node.address = hashlib.sha256(str(i).encode()).hexdigest()
        node.recvBlock(gen_block)
        nodes.append(node)
    return True


def broadcast_transaction(transaction):
    for node in nodes:
        node.recvTransactions(transaction)
        print(f"Transaction broadcasted to node: {node.address}")
    return True


def broadcast_block(block, miner_index):
    recipients = []
    for i, node in enumerate(nodes):
        if node.recvBlock(block):
            recipients.append(i)
    return recipients


def create_transactions():
    transactions = []
    for i in range(nodeCount):
        if random.randint(0, 1) > 0:
            sender = nodes[i]
            if sender.balance < 1:
                continue

            sel = i
            while sel == i:
                sel = random.randint(0, nodeCount - 1)

            recipient = nodes[sel]
            amount = random.randint(1, sender.balance)
            transaction = sender.sendTo(recipient.address, amount)
            broadcast_transaction(transaction)
            transactions.append({
                'from': i,
                'to': sel,
                'amount': amount
            })
            print(f"Transaction created: Node {i} -> Node {sel}, Amount: {amount}")
    return transactions


def mining_process():
    for repeat in range(limit):
        transactions = create_transactions()

        # Print transactions
        if transactions:
            print("\nTransactions this round:")
            for tx in transactions:
                print(f"  Node {tx['from']} -> Node {tx['to']}: {tx['amount']}")

        miner_index = random.randint(0, nodeCount - 1)
        miner = nodes[miner_index]
        candidate_block = miner.doMining()

        # Add mining reward transaction
        reward_tx = {
            'miner': miner_index,
            'amount': reward
        }
        transactions.append(reward_tx)

        recipients = broadcast_block(candidate_block, miner_index)

        current_block = {
            'miner_index': miner_index,
            'recipients': recipients,
            'block_number': repeat + 1
        }

        block_info = [
            f'+ Mining block {repeat + 1} --------- {datetime.datetime.fromtimestamp(candidate_block["time"])}',
            f'hash: {hashlib.sha256(json.dumps(candidate_block).encode()).hexdigest()}',
            f'nonce: {candidate_block["nonce"]}'
        ]

        print(block_info[0])
        print(block_info[1])
        print(block_info[2])

        view.draw(nodes, current_block, block_info, transactions)


if __name__ == "__main__":
    init()
    mining_process()

# 블록체인과 노드의 잔고를 확인하려면 주석을 해제하세요
# for c in nodes[0].chain:
#     print(c)
# for node in nodes:
#     print(node.balance)
