// test1.sol
// SPDX-License-Identifier: MIT
pragma solidity 0.8.6;
import "libraries/utils.sol";
contract Test1 {
    using Utils for uint;
    function add2(uint x)pure public returns(uint){
	return Utils.add2(x);
    }
}
