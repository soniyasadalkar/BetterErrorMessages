class InputClass
{
    private:
			
    public:
	InputClass();
	InputClass(int a,int b);
        ~InputClass();
        InputClass(const InputClass& ic);
        InputClass& operator=(const InputClass& ic);
    	InputClass& operator+(const InputClass& ic);
	InputClass operator--(int i);
};

class A
{
    private:
	    A& operator*(const A& a);
    public:
		A();
		~A();
		A(const A& a);
		A& operator=(const A& a);
		A operator+(const A& a);
};

class B 
{
	public:	
		B(); 
		~B();
		B(const B& b);
		B& operator=(const B& b);
		B& operator++();
};

class C : public A,public B
{
	public:
		void operator()();
};

class FriendFuncClass
{
	private:
		int a;
		int b;
	public:
		FriendFuncClass();
		~FriendFuncClass();
		FriendFuncClass(const FriendFuncClass& ic);
		FriendFuncClass& operator=(const FriendFuncClass& ic);
		friend FriendFuncClass operator*(const FriendFuncClass&,const FriendFuncClass&);
	    
};

