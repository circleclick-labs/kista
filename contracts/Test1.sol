// test1.sol
// SPDX-License-Identifier: MIT
pragma solidity >=0.8.6;
import "libraries/utils.sol";
contract Test1 {
    using Utils for uint;

    string public s;
       
    constructor(string memory s_){
	s = s_;
    }
    
    function add2(uint x) pure public returns(uint){
	return Utils.add2(x);
    }

    address public msgSender;

    function setMsgSender() public {
        msgSender = msg.sender;
    }

    function getMsgSender() view public returns(address){
	return msg.sender;
    }

    function sets(string memory s_) public{
	s = s_;
    }
}
