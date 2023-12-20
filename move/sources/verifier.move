module my_addrx::DeNuVModule{ 

    use 0x1::signer;
    use 0x1::simple_map::{Self, SimpleMap};
    use std::hash;
    use std::vector;
    // use std::string::{String,bytes};

    /// Error codes

    struct DeNuVMap has key {
        map: SimpleMap<u64, address>,
    }

    struct Task has store, drop, copy {
        phone: u64,
        verified: bool,
        otp_hash: vector<u8>,
    }

    struct VerificationPool has key {
        tasks: SimpleMap<address, Task>,
    }

    public fun assert_is_owner(addr: address) {
        assert!(addr == @my_addrx, 0);
    }

    public entry fun initialize_platform(acc: &signer) {
        let addr = signer::address_of(acc);

        assert_is_owner(addr);
        assert!(!exists<VerificationPool>(addr), 0);
        assert!(!exists<DeNuVMap>(addr), 0);

        let v_pool = VerificationPool {
            tasks: simple_map::create(),
        };
        move_to(acc, v_pool);

        let nuids = DeNuVMap {
            map: simple_map::create(),
        };
        move_to(acc, nuids);
    }

    #[event]
    struct VerificationEvent has drop, store {
        account: address,
        phone: u64,
    }

    public entry fun apply(acc: &signer, phone_no:u64) acquires VerificationPool, DeNuVMap {
        let addr = signer::address_of(acc);

        let nuids = borrow_global_mut<DeNuVMap>(@my_addrx);
        assert!(!simple_map::contains_key(&mut nuids.map, &phone_no), 0);

        let v_pool = borrow_global_mut<VerificationPool>(@my_addrx);
        let task = Task {
            phone: phone_no,
            verified: false,
            otp_hash: vector::empty<u8>(),
        };
        simple_map::add(&mut v_pool.tasks, addr, task);
        let v_event = VerificationEvent {
            account: addr,
            phone: phone_no,
        };
        0x1::event::emit(v_event);
    }

    public entry fun submit_otp(acc: &signer, user: address, otp_hash: vector<u8>) acquires VerificationPool {
        let addr = signer::address_of(acc);
        assert_is_owner(addr);
        let v_pool = borrow_global_mut<VerificationPool>(@my_addrx);
        assert!(simple_map::contains_key(&mut v_pool.tasks, &user), 0);
        let task = simple_map::borrow_mut(&mut v_pool.tasks, &user);
        assert!(vector::is_empty<u8>(&task.otp_hash), 0);

        task.otp_hash = otp_hash;
    }

    public entry fun verify(acc: &signer, otp: vector<u8>) acquires VerificationPool, DeNuVMap {
        let addr = signer::address_of(acc);
        let v_pool = borrow_global_mut<VerificationPool>(@my_addrx);
        assert!(simple_map::contains_key(&mut v_pool.tasks, &addr), 0);
        let task = simple_map::borrow_mut(&mut v_pool.tasks, &addr);
        assert!(!task.verified, 0);
        assert!(task.otp_hash == hash::sha2_256(otp), 0);
        task.verified = true;
        
        let nuids = borrow_global_mut<DeNuVMap>(@my_addrx);
        simple_map::add(&mut nuids.map, task.phone, addr);
    }

    #[view]
    public fun get_acc(phone_no: u64): address acquires DeNuVMap {
        let nuids = borrow_global_mut<DeNuVMap>(@my_addrx);
        assert!(simple_map::contains_key(&mut nuids.map, &phone_no), 0);
        let addr = simple_map::borrow_mut(&mut nuids.map, &phone_no);
        *addr
    }

}
