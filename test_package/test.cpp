#include <sphinxclient.h>

int
main(int argc, char* argv[])
{
	sphinx_client* cli = sphinx_create(false);
	sphinx_destroy(cli);
	return 0;
}

