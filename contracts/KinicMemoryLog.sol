// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title KinicMemoryLog
 * @notice Stores human-readable metadata about Kinic memory operations on Monad
 * @dev Logs rich semantic data (title, summary, tags) for each memory interaction
 */
contract KinicMemoryLog {
    struct Memory {
        address user;           // User/agent address
        uint8 opType;          // 0=INSERT, 1=SEARCH
        string title;          // Extracted title (max 100 chars)
        string summary;        // Content summary (max 200 chars)
        string tags;           // Comma-separated keywords
        bytes32 contentHash;   // SHA256 of full content
        uint256 timestamp;     // Block timestamp
    }

    Memory[] public memories;
    mapping(address => uint256[]) public userMemories;

    event MemoryLogged(
        uint256 indexed id,
        address indexed user,
        uint8 opType,
        string title,
        string tags
    );

    /**
     * @notice Log a memory operation with rich metadata
     * @param opType 0 for INSERT, 1 for SEARCH
     * @param title Extracted title or heading
     * @param summary Short summary of content
     * @param tags Comma-separated keywords
     * @param contentHash SHA256 hash of full content
     * @return id The memory ID
     */
    function logMemory(
        uint8 opType,
        string memory title,
        string memory summary,
        string memory tags,
        bytes32 contentHash
    ) external returns (uint256) {
        require(opType <= 1, "Invalid operation type");
        require(bytes(title).length > 0, "Title required");
        require(bytes(title).length <= 100, "Title too long");
        require(bytes(summary).length <= 200, "Summary too long");

        uint256 id = memories.length;

        memories.push(Memory({
            user: msg.sender,
            opType: opType,
            title: title,
            summary: summary,
            tags: tags,
            contentHash: contentHash,
            timestamp: block.timestamp
        }));

        userMemories[msg.sender].push(id);

        emit MemoryLogged(id, msg.sender, opType, title, tags);

        return id;
    }

    /**
     * @notice Get a specific memory by ID
     * @param id Memory ID
     * @return Memory struct
     */
    function getMemory(uint256 id) external view returns (Memory memory) {
        require(id < memories.length, "Invalid memory ID");
        return memories[id];
    }

    /**
     * @notice Get total number of memories logged
     */
    function getTotalMemories() external view returns (uint256) {
        return memories.length;
    }

    /**
     * @notice Get number of memories for a specific user
     * @param user User address
     */
    function getUserMemoryCount(address user) external view returns (uint256) {
        return userMemories[user].length;
    }

    /**
     * @notice Get memory IDs for a specific user
     * @param user User address
     * @return Array of memory IDs
     */
    function getUserMemoryIds(address user) external view returns (uint256[] memory) {
        return userMemories[user];
    }
}
