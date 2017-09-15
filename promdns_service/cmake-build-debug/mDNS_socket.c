//
// Created by zhoushangyue on 17-7-20.
//
#include<sys/types.h>
#include<sys/socket.h>
#include<unistd.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include "mDNS_socket.h"

int mDNS_establish()
{
    int fd=-1;

    struct sockaddr_in local_addr;
    struct ip_mreq mreq;

    bzero(&local_addr,sizeof(local_addr));
    bzero(&mreq,sizeof(struct ip_mreq));


    local_addr.sin_family = AF_INET;
    local_addr.sin_port = htons(5353);
    local_addr.sin_addr.s_addr = INADDR_ANY;

    if ((fd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Unable to create socket\n");
        exit (-1);
    }

    if (bind(fd, (struct sockaddr *)&local_addr, sizeof(struct sockaddr_in)) < 0) {
        perror("Unable to bind socket to interface.n");
        close(fd);
        exit(-2);
    }

    /**join Multicast Group**/
    int loop = 1;
    if (setsockopt(fd, IPPROTO_IP, IP_MULTICAST_LOOP, &loop, sizeof(unsigned char)) == -1) {
        perror("Error calling setsockopt for IP_MULTICAST_LOOPn");
    }
    int ttl = 255;
    if (setsockopt(fd, IPPROTO_IP, IP_MULTICAST_TTL, &ttl, sizeof(unsigned char)) == -1) {
        perror("Error calling setsockopt for IP_MULTICAST_TTLn");
        close(fd);
        exit(-3);
    }
    mreq.imr_multiaddr.s_addr = inet_addr(MDNS_IP);
    mreq.imr_interface.s_addr = htonl(INADDR_ANY);
    if (setsockopt(fd, IPPROTO_IP, IP_ADD_MEMBERSHIP, &mreq, sizeof(struct ip_mreq)) == -1) {
        perror("Error calling setsockopt for IP_ADD_MEMBERSHIPn");
        close(fd);
        exit(-3);
    }
    /**join Multicast Group**/
    return fd;
};//建立套接字

int mDNS_sendmessage(int fd,char *buffer,int packet_len)
{
    struct sockaddr_in server_addr;
    bzero(&server_addr, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr(MDNS_IP);
    server_addr.sin_port = htons(MDNS_PORT);
    if(sendto(fd,buffer,packet_len,0,(struct sockaddr*)&server_addr,sizeof(server_addr))<0)
    {
        perror("Send File Name Failed:");
        exit(-4);
    }
}//像套接字发送制定长度数据包；



