//
// Created by zhoushangyue on 17-6-29.
//

#ifndef PROMDNS_SERVICE_MDNS_H
#define PROMDNS_SERVICE_MDNS_H

#include <sys/param.h>
#define Debug
#define NOTEXIST 9999
#define BUFF_MAX_SIZE 10240

typedef struct{
    char name[100];
    char service_domain[100];
    u_int16_t type;
    char data[100];
    u_int16_t priority;
    u_int16_t weight;
    u_int16_t port;
}mDNS_resource;

typedef struct{
    u_int16_t TRANSACTION;
    u_int16_t FLAGS;
    u_int16_t QUESTION_COUNT;
    u_int16_t ANSWER_COUNT;
    u_int16_t AUTHORITY_COUNT;
    u_int16_t ADDITONAL_COUNT;
}mDNS_HEADER;

typedef struct {
    char *name;
    u_int16_t type;
    u_int16_t class;
    u_int32_t ttl;
    u_int16_t length;
    char *rdata;
}RRecord;

typedef struct {
    char *name;
    u_int16_t type;
    u_int16_t class;
}QRecord;

typedef struct {
    mDNS_HEADER header;
    QRecord question[10];
    RRecord responder[30];
}mDNS_PACKET;

void free_packet(mDNS_PACKET *pa);

void ip4_PTR(char *iptr,char* ip);


void mDNS_startup(int socket_fd,char *hostname,char *ip);

void Probe(int socket_fd,mDNS_resource r);

void Annouce(int socket_fd,char *hostname,char* ip,mDNS_resource r1);

void set_mDNSheader(mDNS_HEADER *header,u_int16_t transaction,u_int16_t flags,
                    u_int16_t questioncnt,u_int16_t answercnt,u_int16_t authoritycnt,
                    u_int16_t additonalcnt);

int set_mDNS_QRecord(QRecord *qr, char *name, u_int16_t type,u_int16_t class);

int set_mDNS_RRecord(RRecord *rr,char *name,char *data,u_int16_t type,u_int16_t class,
                     u_int32_t ttl,u_int16_t length,
                     u_int16_t priority,u_int16_t weight,u_int16_t port);

void write_data(mDNS_PACKET pa,char* buffer);


#endif //PROMDNS_SERVICE_MDNS_H
