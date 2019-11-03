#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define FAIL 0
#define SUCCESS 1 
#define MAX_INT 2147483647
#define MAX_NUM_COUNT 64
#define MAX_OP_COUNT 64

typedef struct
{
	int stak[MAX_NUM_COUNT+1];
	int count;
} Stack_i; // int stack

typedef struct
{
	char stak[MAX_NUM_COUNT+1];
	int count;
} Stack_c; // char stack



char operator_list[] = {'+', '-', '*', '/'} ;

// Globals
Stack_i num_stack;
int curr_num_stack;
Stack_c op_stack;
int curr_op_stack;


/*************************
 * String Manipulation 
 *************************/

// strlen delimited by '\n' or '\0'
int get_str_end(char* str) 
{
    int num = 0 ;
    
    while ( str[num] != 0 ) {
        if ( str[num] == '\n' ) {
            str[num] = '\0' ;
            break ;
        }
        num++ ;
    }
    return num ;
}

// str: pointer to string
// len: length of string
// reverses the order of the string
void reverse(char *str, int len)
{
	int st = 0;
	int end = len - 1;

	while (st < end)
	{
		char c;
		c = str[end];
		str[end] = str[st];
		str[st] = c;

		st++;
		end--;
	}
}



// pass in the num
// returns the str
int itos(int num, char *str)
{
	int is_neg = 0;

	if (num == 0)
	{
		str[0] = '0';
		str[1] = '\0';
		return SUCCESS;
	}

	if (num < 0)
	{
		is_neg = 1;
		num *= -1;
	}

	int i = 0;
	while (num != 0)
	{
		int rem = num % 10;
		str[i++] = (rem > 9) ? (rem - 10) : rem + '0';
		num = num/10; 
	}

	if (is_neg)
	{
		str[i++] = '-';
	}

	
	reverse(str,i);
	str[i] = '\0';

	return SUCCESS;
}

// number string to integer
// str is the incoming string to get the value from
// moved is the number of characters long this number was
// returns the number
int stoi(char *str, int *moved)
{
	int num = 0;
	int i = 0;
	int len = 0;
	while (str[len] <= '9' && str[len] >= '0')
	{
		//printf("char to find len: %c\n", str[len]);
		len++;
	}
	*moved = len;

	for (i = 0; i < len; i++)
	{
		num = num * 10 + (str[i] - '0');
	}
	//printf("stoi: %offset %d: %c to %d\n", len, *str, num);

	return num;
}


/*************************
 * Random 
 *************************/



// min to max , inclusive, min cannot be 0
uint32_t random_in_range(uint32_t min, uint32_t max)
{
    int fd, r;
    uint32_t result, tmp;
    if ( max <= min ) return 0 ;
    
    fd = open("/dev/urandom", O_RDONLY) ;
    if ( (r = read(fd, &tmp, sizeof(tmp))) < 4 ) {
        fprintf(stderr, "random_in_range: read failed\n") ;
    }
    result = min + tmp % ( max - min + 1 ) ;

    return result ;    
}

/*************************
 * Operation stack and Number stack 
 *************************/


int push_num(int num)
{
	// printf("PUSH_NUM: %d\n", num);
	if (curr_num_stack >= MAX_NUM_COUNT)
		return FAIL;
	num_stack.stak[++curr_num_stack] = num;
	return SUCCESS;
}

// returns SUCCESS or FAIL
// pass in number which will contain the requested number
// removes number from num_stack
int pop_num(int *num)
{
	// printf("POP_NUM: %d\n", num_stack.stak[curr_num_stack]);
	if (curr_num_stack <= -1)
	{
		// error, empty
		// printf("POP_NUM failed\n");
		exit(0);
		return FAIL;

	}
	*num = num_stack.stak[curr_num_stack--];
	return SUCCESS;
}

// returns SUCCESS or FAIL
// pass in char pointer which will contain the requested operator
// does NOT remove operator from op_stack
int peek_op(char *op)
{
	if (curr_op_stack <= -1)
	{
		// error, empty
		return FAIL;
	}
	*op = op_stack.stak[curr_op_stack];
	return SUCCESS;
}

// returns SUCCESS or FAIL
// pushes op onto the op_stack
int push_op(char op)
{
	// printf("PUSH_OP: %c\n", op);
	if (curr_op_stack >= MAX_NUM_COUNT)
		return FAIL;
	op_stack.stak[++curr_op_stack] = op;
	return SUCCESS;
}

// returns SUCCESS or FAIL
// pass in char pointer which will contain the requested operator
// removes operator from op_stack
int pop_op(char *op)
{
	// printf("POP_OP: %c\n", op_stack.stak[curr_op_stack]);
	if (curr_op_stack <= -1)
	{
		// error, empty
		// printf("POP_OP failed\n");
		exit(0);
		return FAIL;
	}
	*op = op_stack.stak[curr_op_stack--];
	return SUCCESS;
}

/*************************
 * Evaluation
 *************************/



// Evaluates a single mathemetical operation
int evaluate(int a, char op, int b, int *answer)
{


	// fprintf(stderr, "Evaluate: %d %c %d\n", a, op, b);
	if (op == '+')
	{
		// check for overflow/underflow
		if ((a > 0 && b > MAX_INT - a) ||
			(a < 0 && b < (-1*MAX_INT) - a))
		{
			return FAIL; // overflow would happen
		}
		*answer = a+b;
		return SUCCESS;
	}
	else if (op == '-')
	{
		// check for overflow/underflow
		if ((a > 0 && b < (-1*MAX_INT) + a) ||
			(a < 0 && b > MAX_INT + a))
		{
			fprintf(stderr, "Overflow detected on subtract\n");
			return FAIL; // overflow would happen
		} 
		*answer = a - b;
		return SUCCESS;
	}
		
	else if (op == '*')
	{
		int64_t x = (int64_t)a*b;
		// check for overflow/underflow
		if ((x > 0x7fffffff) || (x < -0x7fffffff))
		{
			return FAIL;
		}
		*answer = a*b;
		return SUCCESS;
	}
		
	else if (op == '/')
	{
		if (b == 0)
			return FAIL; // divide by zero

		*answer = a/b;
		return SUCCESS;
	}
		
	return FAIL;
}


// Solves the equation within a set of parenthesis 
// returns SUCCESS or FAIL
int satisfy_paren()
{
	char op;
	int larg;
	int rarg;
	int answer;
	int ret;

	ret = peek_op(&op);
	while (op != '(' && ret == SUCCESS)
	{
		
		// evaluate everything inside of the parens
		if (pop_num(&rarg) != SUCCESS) return FAIL;
		if (pop_num(&larg) != SUCCESS) return FAIL;
		if (pop_op(&op) != SUCCESS) return FAIL;
		if (evaluate(larg, op, rarg, &answer) != SUCCESS) return FAIL;
		
		// fprintf(stderr, "inside paren loop: %d%c%d=%d\n", larg, op, rarg, answer);
		
		push_num(answer);
		ret = peek_op(&op);
	}
	if (op == '(')
	{
		pop_op(&op); // consume the open paren
	}
	return ret;
}



// Solves the equation in 'str'
// returns SUCCESS if equation was solved
// returns FAIL if equation couldn't be solved
// Solution returned in 'answer'
int solve_equation(char* str, int *answer)
{
	int j = 0;
	int ret;
	char curr;

	// intialize stack
	curr_num_stack = -1;
	curr_op_stack = -1;

	while (str[j] != 0)
	{
		curr = str[j];
		// walk through the equation
		if (curr <= '9' && curr >= '0')
		{
			char t;
			int is_neg = 0;
			int val;
			// get the number (could be any number of spots)
			// this is a number, push it on the stack

			ret = peek_op(&t);
			if (ret == SUCCESS && t == '-')
			{
				if(pop_op(&t) != SUCCESS) return FAIL;
				push_op('+');
				is_neg = 1;
			}
			int moved = 0;
			val = stoi(str+j, &moved);
	
			if (is_neg)
				val *= -1;
			is_neg = 0;

			push_num(val);
			//tmp = get_str_end(str+j);
			j += moved; 
			continue;		
		}
		if (curr == '(')
		{
			push_op(str[j]);
			j++;
			continue;
		}
		if (curr == ')')
		{
			if (satisfy_paren() != SUCCESS) return FAIL;
			j++;
			continue;
		}
		if (curr == '+' || curr == '-')
		{
			char p_op;
			ret = peek_op(&p_op);
			if (ret == SUCCESS && (p_op == '+' || p_op == '-' || p_op == '*' || p_op == '/'))
			{
				char prev_op;
				int larg, rarg, answer = 0;
				if (pop_num(&rarg)!= SUCCESS) return FAIL;
				if (pop_num(&larg)!= SUCCESS) return FAIL;
				if (pop_op(&prev_op)!= SUCCESS) return FAIL;
				if (evaluate(larg, prev_op, rarg, &answer) != SUCCESS) return FAIL;
				push_num(answer);
			}
			push_op(str[j]);
			j++;
			continue;
		}
		if (curr == '*' || curr == '/')
		{
			char prev_op;
			ret = peek_op(&prev_op);
			if (ret == SUCCESS && (prev_op == '*' || prev_op == '/'))
			{
				int larg, rarg, answer = 0;
				if (pop_num(&rarg)!= SUCCESS) return FAIL;
				if (pop_num(&larg)!= SUCCESS) return FAIL;
				if (pop_op(&prev_op)!= SUCCESS) return FAIL;
				if (evaluate(larg, prev_op, rarg, &answer) != SUCCESS) return FAIL;
				push_num(answer);
			}
			push_op(str[j]);
			j++;
			continue;
		}
		return FAIL; // Invalid input. 
			
	}

	int b,a, tmp;
	pop_num(&b);
	while(curr_op_stack != -1)
	{
		if (pop_num(&a)!= SUCCESS) return FAIL;
		if (pop_op(&curr)!= SUCCESS) return FAIL;
		if (evaluate(a,curr,b, &tmp)!= SUCCESS) return FAIL;
		b = tmp;
	}
	*answer = b;
		
	return SUCCESS;
}


// Generate a single equation that will pass validity checks
// Returns answer to that equation
int generate_one_equation(char *equation)
{
	int success, answer;
	do
	{
		char last_op = '\0';
		int last_num = 1;
		int eq_it = 0; // iterator for the equation

		// number of operands
		int num_ops = random_in_range(4,15);

		// number of numbers in this equation
		int num_nums = num_ops + 1; 

		// number of parens
		int num_parens = random_in_range(0,num_ops); 
		// simplest way to add parens is to put all opening parens in the first half of the equation
		//  and the closing parens in the second half of the equation

		// keep track of how many parens we've inserted already
		int opening_parens_inserted = 0; 
		int closing_parens_inserted = 0;

		// alternate between placing a number and an operator
		int turn = 0; // 0: num, 1: operator

		int curr_num = 0; // track how many numbers written

		// construct the equation
		// go for the number of numbers in the equation
		for (curr_num = 0; curr_num < num_nums;)
		{
			if (turn == 0)
			{
				// insert a number
				if (curr_num < num_nums/2)// put them in the first half
				{
					// when adding number in first half, do this
					if (opening_parens_inserted < num_parens)
					{
						// add opening paren before a number
						equation[eq_it++] = '(';
						opening_parens_inserted++;
					}
				}

				// insert number here
				int num = random_in_range(1,256);
				if (last_op == '/')
				{
					num = random_in_range(1,last_num);
				}
				last_num = num;
				char s_num[15]; 
				itos(num, s_num);
	
				int len = get_str_end(s_num);
				for (int z = 0; z < len; z++)
				{
					equation[eq_it++] = s_num[z];
				}

				if (curr_num + 1 > num_nums/2)// put them in the second half
				{
					// when adding number in second half, do this
					if (closing_parens_inserted < opening_parens_inserted)
					{
						// add closing paren after a number
						equation[eq_it++] = ')';
						closing_parens_inserted++;
					}
				}

				turn = 1; // switch to operator
				curr_num++;
			}
			else
			{
				// insert random operator here from operator_list
				int sel = random_in_range(0,3);
				char op = operator_list[sel];
				last_op = op;
				equation[eq_it++] = op;
				turn = 0; // switch to number
			}
		}
		while(closing_parens_inserted < opening_parens_inserted)
		{
			equation[eq_it++] = ')';
			closing_parens_inserted++;
		}
		equation[eq_it] = '\0';

		printf("GENERATE EQUATION:\n");

		printf("# ops: %d\n# nums: %d\n# parens: %d\n", num_ops, num_nums, num_parens);

		printf("Equation: %s\n", equation);

		answer = 0;
		success = solve_equation(equation, &answer);
		if (success != SUCCESS)
		{
			fprintf(stderr, "Invalid equation generated, trying again...\n");
		}
	} while ((success != SUCCESS) || (answer == 0));
	return answer;
}

int
main(int argc, char** argv) {
    char equation[256] ;
    char user_input_buf[256] ;
    uint32_t round = 2;
    int answer, user_answer ;
    int r ;
    while (round--) {
        memset(equation, 0, sizeof(equation)) ;
        answer = generate_one_equation(equation);
        memset(user_input_buf, 0, sizeof(user_input_buf)) ;
        if ((r = read(0, user_input_buf, sizeof(user_input_buf)-1)) < 0 ) {
            fprintf(stderr, "read failure\n") ;
        }
        user_answer = atoi(user_input_buf) ;
        printf("%s Answers\n", answer==user_answer? "Correct": "Wrong");
        printf("answer == %d\n\n\n", answer ) ;
    }
    return 0 ;
}
