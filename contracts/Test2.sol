// test1.sol
// SPDX-License-Identifier: MIT
pragma solidity >=0.8.6;
import "libraries/utils.sol";
contract Test2 {
    using Utils for uint;

    string public s;
       
    constructor(string memory s_){
	s = s_;
    }
 
    uint256 public val0;
    uint256 public val1;
    uint256 public val2;
    function vals() view public returns(uint256 v0,
					uint256 v1,
					uint256 v2) {
	(v0, v1, v2) = (val0, val1, val2);
    }
    function dontPayMe(uint256 x) external {
	val0 = x;
    }
    function payMe(uint256 x) external payable {
	val1 = msg.value;
	val2 = x;
	require(x == msg.value, "no");
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
