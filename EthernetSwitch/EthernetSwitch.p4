/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

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
            default: accept; // TODO Reject the frame
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

    /* Broadcast implementation
    TODO implement it in the json file
    action broadcast() {
        modify_field(intrinsic_metadata.mgid, 1);
    }
    */

    //-- TABLES --//
    /* -- May be implemented later, it corresponds to MAC adress learning
    table smac {
        key = {
            hdr.ethernet.srcAddr : exact;
        }
        actions = {
            mac_learn; // evaluate pertinence
        }
        size = 512;
    }
    */
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
        size = 1024;
        default_action = drop();
    }
    apply {
        // static forwarding
        if (hdr.ethernet.isValid()) {
            dmac.apply();
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
