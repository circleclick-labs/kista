// test1.sol
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.6;
contract erc20 {
    string public name;
    string public symbol;
    uint8  public decimals;
    uint   public totalSupply;
    mapping(address=>uint) public balanceOf;
    mapping(address=>mapping(address=>uint)) public allowance;
    event Approval(address indexed owner, address indexed spender, uint amount);
    event Transfer(address indexed from,  address indexed to,      uint amount);
    function approve(address _spender, uint256 _amount)
	public returns (bool success) {
	allowance[msg.sender][_spender] = _amount;
	emit Approval(msg.sender, _spender, _amount);
	return true;
    }
    function transfer(address _to, uint256 _amount)
	public returns (bool success) {
	if((balanceOf[msg.sender] >= _amount))
	    {
		balanceOf[msg.sender] -= _amount;
		balanceOf[_to] += _amount;
		emit Transfer(msg.sender, _to, _amount);
		return true;
	    }
    }
    function transferFrom(address _from, address _to, uint256 _amount)
	public returns (bool success) {
	if((balanceOf[_from] >= _amount &&
	    allowance[_from][msg.sender] >=
	    _amount && _amount > 0 &&
	    balanceOf[_to] + _amount > balanceOf[_to]))
	    {
		balanceOf[_from] -= _amount;
		balanceOf[_to] += _amount;
		emit Transfer(_from, _to, _amount);
		return true;
	    }
    }
    constructor(string memory _name, string memory _symbol,
		uint8 _decimals, uint _totalSupply) {
	name=_name;
	symbol=_symbol;
	decimals = _decimals;
	balanceOf[msg.sender] = totalSupply = _totalSupply;
	emit Transfer(address(0), msg.sender, _totalSupply);
    }
}
