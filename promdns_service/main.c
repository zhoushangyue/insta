
#include <netdb.h>
#include "./cmake-build-debug/mDNS.h"
#include "cmake-build-debug/mDNS_socket.h"
#include "cmake-build-debug/mDNS.h"
#include <unistd.h>
#include <string.h>

int main(int argc ,char *argv[]) {
    int socket_fd=mDNS_establish();
    mDNS_resource r1;
    strncpy(r1.name,"pro110._osc._tcp.local",strlen("shangyue._osc._tcp.local"));
    strncpy(r1.service_domain,"_osc._tcp.local",strlen("_osc._tcp.local"));
    strncpy(r1.data,"zhoushangyue-ThinkPad-E470c.local",strlen("zhoushangyue-ThinkPad-E470c.local"));
    r1.type=33;
    r1.port=80;
    r1.priority=0;
    r1.weight=0;


    mDNS_startup(socket_fd,"zhoushangyue-ThinkPad-E470c.local","192.168.2.4");

    Probe(socket_fd,r1);

    Annouce(socket_fd,"zhoushangyue-ThinkPad-E470c.local","192.168.2.4",r1);

    close(socket_fd);
    return 0;
}