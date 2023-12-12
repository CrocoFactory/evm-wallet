from web3 import Web3

ZERO_ADDRESS = Web3.to_checksum_address("0x0000000000000000000000000000000000000000")

NETWORK_MAP = {
    'Arbitrum Goerli': {
        'chain_id': 421613,
        'rpc': 'https://arbitrum-goerli.publicnode.com',
        'token': 'AGOR',
        'explorer': 'https://goerli.arbiscan.io'
    },
    'Arbitrum': {
        'chain_id': 42161,
        'rpc': 'https://arbitrum-one.publicnode.com',
        'token': 'ETH',
        'explorer': 'https://arbiscan.io'
    },
    'Avalanche': {
        'chain_id': 43114,
        'rpc': 'https://avalanche-c-chain.publicnode.com',
        'token': 'AVAX',
        'explorer': 'https://snowtrace.io/'
    },
    'Base': {
        'chain_id': 8453,
        'rpc': 'https://base.publicnode.com',
        'token': 'ETH',
        'explorer': 'https://basescan.org/'
    },
    'Base Goerli': {
        'chain_id': 84531,
        'rpc': 'https://base-goerli.publicnode.com',
        'token': 'ETH',
        'explorer': 'https://goerli.basescan.org/'
    },
    'BSC': {
        'chain_id': 56,
        'rpc': 'https://bsc.publicnode.com',
        'token': 'BNB',
        'explorer': 'https://bscscan.com'
    },
    'BSC Testnet': {
        'chain_id': 97,
        'rpc': 'https://bsc-testnet.publicnode.com',
        'token': 'tBNB',
        'explorer': 'https://testnet.bscscan.com'
    },
    'Ethereum': {
        'chain_id': 1,
        'rpc': 'https://ethereum.publicnode.com',
        'token': 'ETH',
        'explorer': 'https://etherscan.io'
    },
    'Fantom': {
        'chain_id': 250,
        'rpc': 'https://fantom.publicnode.com',
        'token': 'FTM',
        'explorer': 'https://ftmscan.com/'
    },
    'Fantom Testnet': {
        'chain_id': 4002,
        'rpc': 'https://fantom-testnet.publicnode.com',
        'token': 'FTM',
        'explorer': 'https://testnet.ftmscan.com/'
    },
    'Fuji': {
        'chain_id': 43113,
        'rpc': 'https://avalanche-fuji-c-chain.publicnode.com',
        'token': 'AVAX',
        'explorer': 'https://testnet.snowtrace.io'
    },
    'Goerli': {
        'chain_id': 5,
        'rpc': 'https://ethereum-goerli.publicnode.com',
        'token': 'GETH',
        'explorer': 'https://goerli.etherscan.io'
    },
    'Linea': {
        'chain_id': 59144,
        'rpc': 'https://linea.drpc.org',
        'token': 'ETH',
        'explorer': 'https://lineascan.build/'
    },
    'Linea Goerli': {
        'chain_id': 59140,
        'rpc': 'https://rpc.goerli.linea.build',
        'token': 'ETH',
        'explorer': 'https://goerli.lineascan.build/'
    },
    'Mumbai': {
        'chain_id': 80001,
        'rpc': 'https://polygon-mumbai-bor.publicnode.com',
        'token': 'MATIC',
        'explorer': 'https://mumbai.polygonscan.com/'
    },
    'opBNB': {
        'chaind_id': 204,
        'rpc': 'https://opbnb.publicnode.com',
        'token': 'BNB',
        'explorer': 'https://opbnb.bscscan.com/'
    },
    'opBNB Testnet': {
        'chaind_id': 5611,
        'rpc': 'https://opbnb-testnet.publicnode.com',
        'token': 'BNB',
        'explorer': 'https://opbnb-testnet.bscscan.com'
    },
    'Optimism': {
        'chain_id': 10,
        'rpc': 'https://optimism.publicnode.com',
        'token': 'ETH',
        'explorer': 'https://optimistic.etherscan.io'
    },
    'Optimism Goerli': {
        'chain_id': 420,
        'rpc': 'https://optimism-goerli.publicnode.com',
        'token': 'OGOR',
        'explorer': 'https://goerli-optimism.etherscan.io'
    },
    'Polygon': {
        'chain_id': 137,
        'rpc': 'https://polygon-bor.publicnode.com',
        'token': 'MATIC',
        'explorer': 'https://polygonscan.com'
    },
    'Sepolia': {
        'chain_id': 11155111,
        'rpc': 'https://ethereum-sepolia.publicnode.com',
        'token': 'SETH',
        'explorer': 'https://sepolia.etherscan.io'
    },
    'zkSync': {
        'chain_id': 324,
        'rpc': 'https://zksync.drpc.org',
        'token': 'ETH',
        'explorer': 'https://explorer.zksync.io'
    }
}
