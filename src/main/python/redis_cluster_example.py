"""
Redis Cluster with Sentinel configuration and examples
Master: redis-master.rgzz:6379
Sentinels: starlight:26379, starlight:26380
"""

from redis.sentinel import Sentinel
import redis

# ============================================================================
# 1. CONNECTION VIA SENTINEL (Recommended for HA)
# ============================================================================

def connect_via_sentinel():
    """
    Connect to Redis using Sentinel for automatic failover
    Sentinel monitors master and handles replication
    """
    # Define sentinel nodes
    sentinels = [
        ('starlight', 26379),
        ('starlight', 26380),
    ]

    # Create Sentinel instance
    sentinel = Sentinel(sentinels, socket_timeout=0.1)

    # Get master connection
    master = sentinel.master_for('mymaster', socket_timeout=0.1)

    # Get slave connection (read-only)
    slave = sentinel.slave_for('mymaster', socket_timeout=0.1)

    return sentinel, master, slave


# ============================================================================
# 2. DIRECT CONNECTION (Without Sentinel)
# ============================================================================

def connect_direct():
    """
    Direct connection to Redis master without Sentinel
    Good for simple setups or testing
    """
    r = redis.Redis(
        host='redis-master.rgzz',
        port=6379,
        decode_responses=True,
        socket_timeout=5
    )
    return r


# ============================================================================
# 3. CONNECTION POOL (Recommended for production)
# ============================================================================

def connect_with_pool():
    """
    Connection using pool for better performance
    """
    pool = redis.ConnectionPool(
        host='redis-master.rgzz',
        port=6379,
        db=0,
        decode_responses=True,
        max_connections=10,
        socket_timeout=5,
        socket_connect_timeout=5,
        retry_on_timeout=True
    )
    r = redis.Redis(connection_pool=pool)
    return r


# ============================================================================
# 4. SENTINEL CONNECTION POOL (Best for HA)
# ============================================================================

def connect_sentinel_with_pool():
    """
    Sentinel connection with connection pool - best practice for production
    Provides automatic failover and load balancing
    """
    sentinels = [
        ('starlight', 26379),
        ('starlight', 26380),
    ]

    sentinel = Sentinel(sentinels, socket_timeout=0.1)

    # Master connection pool
    master = sentinel.master_for(
        'mymaster',
        socket_timeout=0.1,
        db=0,
        decode_responses=True
    )

    # Slave connection pool (for read operations)
    slave = sentinel.slave_for(
        'mymaster',
        socket_timeout=0.1,
        db=0,
        decode_responses=True
    )

    return sentinel, master, slave

def generate_test_data(master_conn, slave_conn=None):
    """
    Generate comprehensive test data in Redis for demonstration purposes
    """
    print("\n" + "="*60)
    print("🔄 GENERATING TEST DATA")
    print("="*60)

    try:
        # ============================================================================
        # 1. STRINGS - Basic key-value pairs
        # ============================================================================
        print("\n📝 Generating STRING data...")

        # User profiles
        master_conn.set('user:alice:name', 'Alice Johnson')
        master_conn.set('user:alice:email', 'alice@example.com')
        master_conn.set('user:alice:age', '28')

        master_conn.set('user:bob:name', 'Bob Smith')
        master_conn.set('user:bob:email', 'bob@example.com')
        master_conn.set('user:bob:age', '34')

        # Session data with TTL
        master_conn.setex('session:abc123', 3600, 'user:alice')
        master_conn.setex('session:def456', 1800, 'user:bob')

        # Counters
        master_conn.set('counter:page_views', '0')
        master_conn.set('counter:api_calls', '0')

        print("✅ STRING data generated")

        # ============================================================================
        # 2. HASHES - User profiles and configurations
        # ============================================================================
        print("\n📊 Generating HASH data...")

        # Detailed user profiles
        master_conn.hset('user:alice:profile', mapping={
            'name': 'Alice Johnson',
            'email': 'alice@example.com',
            'age': '28',
            'city': 'New York',
            'occupation': 'Software Engineer',
            'joined': '2023-01-15',
            'last_login': '2024-01-14'
        })

        master_conn.hset('user:bob:profile', mapping={
            'name': 'Bob Smith',
            'email': 'bob@example.com',
            'age': '34',
            'city': 'San Francisco',
            'occupation': 'Product Manager',
            'joined': '2022-08-20',
            'last_login': '2024-01-13'
        })

        # Configuration settings
        master_conn.hset('config:app', mapping={
            'debug_mode': 'false',
            'max_connections': '100',
            'timeout': '30',
            'cache_enabled': 'true'
        })

        master_conn.hset('config:database', mapping={
            'host': 'localhost',
            'port': '5432',
            'max_pool_size': '20',
            'ssl_enabled': 'true'
        })

        print("✅ HASH data generated")

        # ============================================================================
        # 3. LISTS - Queues, logs, recent activities
        # ============================================================================
        print("\n📋 Generating LIST data...")

        # User activity logs
        master_conn.lpush('activity:alice', 'login:2024-01-14 10:30:00')
        master_conn.lpush('activity:alice', 'view_profile:2024-01-14 10:25:00')
        master_conn.lpush('activity:alice', 'update_settings:2024-01-14 10:20:00')
        master_conn.lpush('activity:alice', 'login:2024-01-13 09:15:00')

        master_conn.lpush('activity:bob', 'login:2024-01-13 14:20:00')
        master_conn.lpush('activity:bob', 'create_post:2024-01-13 14:15:00')
        master_conn.lpush('activity:bob', 'login:2024-01-12 11:30:00')

        # Task queues
        master_conn.lpush('queue:email', 'user:alice:registration')
        master_conn.lpush('queue:email', 'user:bob:password_reset')
        master_conn.lpush('queue:email', 'admin:weekly_report')

        master_conn.lpush('queue:notifications', 'alice:friend_request')
        master_conn.lpush('queue:notifications', 'bob:like_received')

        # Recent searches
        master_conn.lpush('recent_searches:alice', 'redis tutorial')
        master_conn.lpush('recent_searches:alice', 'python async')
        master_conn.lpush('recent_searches:alice', 'docker compose')

        print("✅ LIST data generated")

        # ============================================================================
        # 4. SETS - Tags, categories, unique items
        # ============================================================================
        print("\n🎯 Generating SET data...")

        # User interests/tags
        master_conn.sadd('tags:alice', 'python', 'redis', 'docker', 'kubernetes', 'microservices')
        master_conn.sadd('tags:bob', 'javascript', 'react', 'aws', 'devops', 'agile')

        # Online users
        master_conn.sadd('online_users', 'alice', 'bob', 'charlie')

        # Categories
        master_conn.sadd('categories:tech', 'programming', 'databases', 'devops', 'cloud')
        master_conn.sadd('categories:business', 'management', 'finance', 'marketing', 'sales')

        # Permissions
        master_conn.sadd('permissions:alice', 'read', 'write', 'admin')
        master_conn.sadd('permissions:bob', 'read', 'write')

        print("✅ SET data generated")

        # ============================================================================
        # 5. SORTED SETS - Rankings, scores, priorities
        # ============================================================================
        print("\n🏆 Generating SORTED SET data...")

        # User scores/rankings
        master_conn.zadd('leaderboard:game1', {'alice': 1500, 'bob': 1200, 'charlie': 1100, 'diana': 1050})
        master_conn.zadd('leaderboard:game2', {'bob': 950, 'alice': 900, 'diana': 850, 'charlie': 800})

        # Task priorities (lower score = higher priority)
        master_conn.zadd('tasks:urgent', {'fix_critical_bug': 1, 'update_security': 2, 'deploy_hotfix': 3})
        master_conn.zadd('tasks:backlog', {'add_feature_x': 10, 'refactor_code': 15, 'write_docs': 20})

        # Product ratings
        master_conn.zadd('ratings:product_123', {'user1': 5, 'user2': 4, 'user3': 5, 'user4': 3})

        print("✅ SORTED SET data generated")

        # ============================================================================
        # 6. COMPLEX DATA STRUCTURES - Real-world examples
        # ============================================================================
        print("\n🏗️ Generating COMPLEX data structures...")

        # Shopping cart (Hash with list of items)
        master_conn.hset('cart:alice', mapping={
            'user_id': 'alice',
            'created': '2024-01-14 10:00:00',
            'total_items': '3',
            'total_price': '149.97'
        })
        master_conn.lpush('cart:alice:items', 'item:1:2', 'item:5:1', 'item:12:1')  # item_id:quantity

        # Blog posts with metadata
        master_conn.hset('post:1', mapping={
            'title': 'Introduction to Redis',
            'author': 'alice',
            'content': 'Redis is an open source in-memory data structure store...',
            'created': '2024-01-10',
            'tags': 'redis,database,tutorial',
            'views': '150',
            'likes': '25'
        })
        master_conn.sadd('post:1:tags', 'redis', 'database', 'tutorial')
        master_conn.zadd('post:1:likes', {'bob': 1640995200, 'charlie': 1641081600})  # user:timestamp

        print("✅ COMPLEX data structures generated")

        # ============================================================================
        # 7. TEST REPLICATION (if slave available)
        # ============================================================================
        if slave_conn:
            print("\n🔄 Testing REPLICATION...")
            import time

            # Write to master
            master_conn.set('replication_test', 'master_data')
            master_conn.incr('counter:replication')

            # Wait for replication
            time.sleep(1)

            # Read from slave
            slave_value = slave_conn.get('replication_test')
            slave_counter = slave_conn.get('counter:replication')

            if slave_value == 'master_data':
                print("✅ Replication working - slave has master data")
            else:
                print("❌ Replication issue - slave data mismatch")

            print(f"   Master counter: {master_conn.get('counter:replication')}")
            print(f"   Slave counter: {slave_counter}")

        print("\n" + "="*60)
        print("🎉 TEST DATA GENERATION COMPLETED!")
        print("="*60)

        # Summary
        total_keys = len(master_conn.keys('*'))
        print(f"\n📊 Summary: Generated approximately {total_keys} keys")

        return True

    except Exception as e:
        print(f"❌ Error generating test data: {e}")
        return False


def clear_test_data(master_conn):
    """
    Clear all test data from Redis
    """
    print("\n🧹 Clearing existing test data...")

    try:
        # Get all keys matching test data patterns
        patterns = [
            'user:*',
            'session:*',
            'counter:*',
            'config:*',
            'activity:*',
            'queue:*',
            'recent_searches:*',
            'tags:*',
            'online_users',
            'categories:*',
            'permissions:*',
            'leaderboard:*',
            'tasks:*',
            'ratings:*',
            'cart:*',
            'post:*',
            'replication_test'
        ]

        total_deleted = 0
        for pattern in patterns:
            keys = master_conn.keys(pattern)
            if keys:
                deleted = master_conn.delete(*keys)
                total_deleted += deleted
                print(f"   Deleted {deleted} keys matching '{pattern}'")

        print(f"✅ Cleared {total_deleted} test keys")
        return True

    except Exception as e:
        print(f"❌ Error clearing test data: {e}")
        return False


def demonstrate_data_operations(master_conn, slave_conn=None):
    """
    Demonstrate various Redis operations on the generated test data
    """
    print("\n" + "="*60)
    print("🔍 DEMONSTRATING REDIS OPERATIONS")
    print("="*60)

    try:
        # ============================================================================
        # STRING OPERATIONS
        # ============================================================================
        print("\n📝 STRING OPERATIONS:")

        # Basic get/set
        name = master_conn.get('user:alice:name')
        print(f"   Alice's name: {name}")

        # TTL operations
        ttl = master_conn.ttl('session:abc123')
        print(f"   Session TTL: {ttl} seconds")

        # Increment counters
        master_conn.incr('counter:page_views')
        master_conn.incrby('counter:api_calls', 5)
        print(f"   Page views: {master_conn.get('counter:page_views')}")
        print(f"   API calls: {master_conn.get('counter:api_calls')}")

        # ============================================================================
        # HASH OPERATIONS
        # ============================================================================
        print("\n📊 HASH OPERATIONS:")

        # Get specific field
        alice_city = master_conn.hget('user:alice:profile', 'city')
        print(f"   Alice's city: {alice_city}")

        # Get all fields
        alice_profile = master_conn.hgetall('user:alice:profile')
        print(f"   Alice's profile: {alice_profile}")

        # Get multiple fields
        config_fields = master_conn.hmget('config:app', ['debug_mode', 'max_connections'])
        print(f"   App config: {config_fields}")

        # ============================================================================
        # LIST OPERATIONS
        # ============================================================================
        print("\n📋 LIST OPERATIONS:")

        # Get list length
        activity_count = master_conn.llen('activity:alice')
        print(f"   Alice's activity count: {activity_count}")

        # Get range of items
        recent_activity = master_conn.lrange('activity:alice', 0, 2)
        print(f"   Alice's recent activity: {recent_activity}")

        # Pop from list (queue operations)
        next_email = master_conn.rpop('queue:email')
        print(f"   Next email to process: {next_email}")

        # ============================================================================
        # SET OPERATIONS
        # ============================================================================
        print("\n🎯 SET OPERATIONS:")

        # Check membership
        has_python = master_conn.sismember('tags:alice', 'python')
        print(f"   Alice has 'python' tag: {has_python}")

        # Get all members
        alice_tags = master_conn.smembers('tags:alice')
        print(f"   Alice's tags: {alice_tags}")

        # Set intersection
        common_tags = master_conn.sinter('tags:alice', 'tags:bob')
        print(f"   Common tags: {common_tags}")

        # ============================================================================
        # SORTED SET OPERATIONS
        # ============================================================================
        print("\n🏆 SORTED SET OPERATIONS:")

        # Get top players
        top_players = master_conn.zrevrange('leaderboard:game1', 0, 2, withscores=True)
        print(f"   Top 3 players: {top_players}")

        # Get score
        alice_score = master_conn.zscore('leaderboard:game1', 'alice')
        print(f"   Alice's score: {alice_score}")

        # Count items in score range
        high_scores = master_conn.zcount('leaderboard:game1', 1200, 2000)
        print(f"   Players with score 1200+: {high_scores}")

        # ============================================================================
        # COMPLEX OPERATIONS
        # ============================================================================
        print("\n🏗️ COMPLEX OPERATIONS:")

        # Multi-key operations
        all_users = master_conn.mget(['user:alice:name', 'user:bob:name'])
        print(f"   All user names: {all_users}")

        # Pipeline operations
        pipe = master_conn.pipeline()
        pipe.get('user:alice:age')
        pipe.hget('user:bob:profile', 'occupation')
        pipe.scard('tags:alice')
        results = pipe.execute()
        print(f"   Pipeline results: age={results[0]}, occupation={results[1]}, tag_count={results[2]}")

        # ============================================================================
        # REPLICATION DEMO (if slave available)
        # ============================================================================
        if slave_conn:
            print("\n🔄 REPLICATION DEMO:")

            # Write to master
            master_conn.set('demo_key', 'written_to_master')

            # Read from slave (should be replicated)
            import time
            time.sleep(0.5)  # Wait for replication
            slave_value = slave_conn.get('demo_key')
            print(f"   Read from slave: {slave_value}")

            # Compare master and slave data
            master_keys = len(master_conn.keys('user:*'))
            slave_keys = len(slave_conn.keys('user:*'))
            print(f"   Master user keys: {master_keys}, Slave user keys: {slave_keys}")

        print("\n" + "="*60)
        print("✅ DEMONSTRATION COMPLETED!")
        print("="*60)

        return True

    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        return False




# ============================================================================
# 5. EXAMPLE USAGE
# ============================================================================

if __name__ == '__main__':
    print("🚀 Redis Cluster Test Script")
    print("=" * 50)

    # Test Sentinel connection
    try:
        print("\n🔗 Testing Sentinel connection...")
        sentinel, master, slave = connect_via_sentinel()

        # Ping master
        print(f"✅ Master ping: {master.ping()}")

        # Ping slave
        print(f"✅ Slave ping: {slave.ping()}")

        # Get sentinel info
        print(f"\n📊 Sentinel info:")
        info = sentinel.sentinel_masters()
        print(f"   Masters: {info}")

        # Interactive menu
        while True:
            print("\n" + "="*50)
            print("🎯 CHOOSE ACTION:")
            print("1. Clear existing test data")
            print("2. Generate new test data")
            print("3. Demonstrate Redis operations")
            print("4. Run full cycle (clear + generate + demo)")
            print("5. Exit")
            print("="*50)

            choice = input("Enter your choice (1-5): ").strip()

            if choice == '1':
                clear_test_data(master)
            elif choice == '2':
                generate_test_data(master, slave)
            elif choice == '3':
                demonstrate_data_operations(master, slave)
            elif choice == '4':
                print("\n🔄 Running full cycle...")
                clear_test_data(master)
                generate_test_data(master, slave)
                demonstrate_data_operations(master, slave)
            elif choice == '5':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-5.")

    except Exception as e:
        print(f"❌ Sentinel connection failed: {e}")
        print("\n🔄 Trying direct connection...")

        try:
            r = connect_direct()
            print(f"✅ Direct connection ping: {r.ping()}")

            # Simple operations with direct connection
            print("\n🔧 Running basic operations with direct connection...")

            # Clear and generate
            clear_test_data(r)
            generate_test_data(r)

            # Basic demo
            print("\n📝 Basic operations demo:")
            print(f"   Alice's name: {r.get('user:alice:name')}")
            print(f"   Bob's email: {r.get('user:bob:email')}")
            print(f"   Online users: {r.smembers('online_users')}")

        except Exception as e2:
            print(f"❌ Direct connection also failed: {e2}")
            print("\n💡 Make sure Redis containers are running:")
            print("   docker-compose up -d redis sentinel-1 sentinel-2")

