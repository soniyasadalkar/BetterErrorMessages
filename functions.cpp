template<typename T1>
void foo(T1 a)
{
	T1 b[10];
	T1 c(10);
	
	c = a();
	c++;
	
	
}

template<typename T2>
T2 bar(T2& a,T2& b)
{
	T2 c;
	T2 d(c);
	c = a + b;
	d = 2 * c;
	return c;
	
}

template<typename T3,typename T4>
T3 multitype(T3 a,T4& b)
{
	
	T4 c[4];
	T3 d(a);
	T3 e(10,20,30);
	a = d();
	T4 g;
	g = b;	
	return e;
}


