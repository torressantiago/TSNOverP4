/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

// #define SET_EGRESS_PORT(value)    standard_metadata.egress_port = (PortId_t)value

const bit<16> TYPE_VLAN = 0x8100;

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

typedef bit<48> macAddr_t;
typedef bit<9>  egressSpec_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header vlan_t {
    bit<16> TPID;
    bit<3> PRI;
    bit<1> CFI;
    bit<12> VID; 
}

struct metadata {
    /* empty */
}

struct headers {
    ethernet_t   ethernet;
    vlan_t vlan;
}

/*************************************************************************
*********************** P A R S E R  *************************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_VLAN : parse_vlan;
            default: accept;
        }
    }

    state parse_vlan {
        packet.extract(hdr.vlan);
        transition accept;
    }

}

/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {   
    apply {  }
}


/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {

    // OBSERVATION : An action must be used if routing or forwarding tables+actions are involved.
    //-- ACTIONS --//
    action drop() {
        mark_to_drop(standard_metadata);
    }

    action forward(egressSpec_t port) {
        standard_metadata.egress_spec = port;
    }

    /* 
    // Broadcast implementation
    // TODO implement it in the json file
    action broadcast() {
        SET_EGRESS_PORT(PortId_const(100)); // Broadcast port
    }

    // MAC learn
    action mac_learn() {
        CALL_DIGEST(mac_learn_digest_t, mac_learn_digest, 1024, ({ hdr.ethernet.srcAddr, GET_INGRESS_PORT() }));
    }

    action _nop() {
    }
    */
     


    //-- TABLES --//
    table dmac {
        key = {
            hdr.ethernet.dstAddr : exact;
        }
        actions = {
            forward; 
            // broadcast;
            drop;
            NoAction;
        }
        size = 512;
        default_action = drop();
    }
    /*
    table smac {
        actions = {
            mac_learn;
            _nop;
            drop;
        }
        key = {
            hdr.ethernet.srcAddr: exact;
        }
        default_action = mac_learn();
        size = 512;
    }
    */
    apply {
        // static forwarding
        if (hdr.ethernet.isValid() && hdr.ethernet.etherType == TYPE_VLAN) {
            //smac.apply();
            dmac.apply();
        }
        else{
            drop();
        }
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply {  }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers  hdr, inout metadata meta) {
     apply {  }
}

/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.vlan);
    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;