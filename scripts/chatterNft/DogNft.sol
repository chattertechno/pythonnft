pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract ChatterNft is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    enum Mood{PUG, SHIBA_INU, ST_BERNARD}
    // add other things
    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIdToTokenURI;
    mapping(uint256 => Mood) public tokenIdToMood;
    mapping(bytes32 => uint256) public requestIdToTokenId;
    event requestedToken(bytes32 indexed requestId); 


    bytes32 internal keyHash;
    uint256 internal fee;
    
    constructor(address _VRFCoordinator, address _LinkToken, bytes32 _keyhash)
    public 
    VRFConsumerBase(_VRFCoordinator, _LinkToken)
    ERC721("Maxim", "max")
    {
        tokenCounter = 0;
        keyHash = _keyhash;
        fee = 0.1 * 10 ** 18;
    }

    function createToken(string memory tokenURI) 
        public returns (bytes32){
            bytes32 requestId = requestRandomness(keyHash, fee);
            requestIdToSender[requestId] = msg.sender;
            requestIdToTokenURI[requestId] = tokenURI;
            emit requestedToken(requestId);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        address chatterOwner = requestIdToSender[requestId];
        string memory tokenURI = requestIdToTokenURI[requestId];
        uint256 newTokenId = tokenCounter;
        _safeMint(chatterOwner, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        Breed breed = Breed(randomNumber % 3); 
        tokenIdTOMood[newTokenId] = breed;
        requestIdToTokenId[requestId] = newTokenId;
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: transfer caller is not owner nor approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
contract SpaceCatsDeployer is ERC721Enumerable, Ownable {
    using Strings for uint256;
    event Mint(address indexed sender, uint256 startWith, uint256 times);

    //supply counters
    uint256 public totalMints;
    uint256 public totalCount = 9999;
   
    //token Index tracker


    uint256 public maxToMint = 10;
    uint256 public price = 0.05 * 10 ** 18;

    //string
    string public baseURI;

    //bool
    bool private started;
    //constructor args
    constructor(string memory name_, string memory symbol_, string memory baseURI_) ERC721(name_, symbol_) {
        baseURI = baseURI_;
    }

    //basic functions.
    function _baseURI() internal view virtual override returns (string memory){
        return baseURI;
    }
    function setBaseURI(string memory _newURI) public onlyOwner {
        baseURI = _newURI;
    }

    //erc721
    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
        require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token.");

        string memory baseURI2 = _baseURI();
        return bytes(baseURI2).length > 0
            ? string(abi.encodePacked(baseURI2, tokenId.toString(), ".json")) : '.json';
    }
    function setStart(bool _start) public onlyOwner {
        started = _start;
    }

    function tokensOfOwner(address owner)
        public
        view
        returns (uint256[] memory)
    {
        uint256 count = balanceOf(owner);
        uint256[] memory ids = new uint256[](count);
        for (uint256 i = 0; i < count; i++) {
            ids[i] = tokenOfOwnerByIndex(owner, i);
        }
        return ids;
    }

    function mint(uint256 _times) payable public {
        require(started, "not started");
        require(_times > 0 && _times <= maxToMint, "You can only mint 10 at a time");
        require(totalMints + _times <= totalCount, "Sold out!");
        require(msg.value == _times * price, "Please send correct amount of ETH");
        
        payable(owner()).transfer(msg.value);
        emit Mint(_msgSender(), totalMints + 1, _times);
        for(uint256 i = 0; i< _times; i++){
            _mint(_msgSender(), 1 + totalMints++);
        }
    }
}