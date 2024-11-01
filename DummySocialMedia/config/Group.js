const db = require('./db'),
  { rmdir } = require('fs'),
  { promisify } = require('util'),
  root = process.cwd(),
  { deletePost } = require('./Post'),
  { DeleteAllOfFolder } = require('handy-image-processor'),
  { intersectionBy } = require('lodash')

/**
 * Returns what of a group
 * @param {String} what Get what, e.g., 'name'
 * @param {Number} group Group ID
 */
const getWhatOfGrp = async (what, group) => {
  try {
    // Use template literal with backticks here for SQL query
    const query = `SELECT ${what} FROM \`groups\` WHERE group_id = ?`;
    
    // Execute the query
    let results = await db.query(query, [group]);
    
    // Check if results are returned
    if (results.length === 0) {
      console.warn(`No results found for group_id: ${group}`);
      return ''; // Return empty string if no results found
    }
    
    return results[0][what]; // Return the desired column value
  } catch (error) {
    console.error('Error in getWhatOfGrp:', error);
    return ''; // Return an empty string on error
  }
};


/**
 * Deletes a group
 * @param {Number} group GroupID
 */
const deleteGroup = async group => {
  try {
    const posts = await db.query('SELECT post_id FROM posts WHERE group_id=?', [group]);
    const dltDir = promisify(rmdir);

    for (let p of posts) {
      await deletePost({ post: p.post_id, when: 'group' });
    }

    await db.query('DELETE FROM notifications WHERE group_id=?', [group]);
    await db.query('DELETE FROM group_members WHERE group_id=?', [group]);
    await db.query('DELETE FROM groups WHERE group_id=?', [group]);

    DeleteAllOfFolder(`${root}/dist/groups/${group}/`);
    await dltDir(`${root}/dist/groups/${group}`);
  } catch (error) {
    console.error('Error in deleteGroup:', error);
  }
};

/**
 * Checks if a user joined the group
 * @param {Number} user UserID
 * @param {Number} group GroupID
 */
const joinedGroup = async (user, group) => {
  try {
    const is = await db.query(
      'SELECT COUNT(grp_member_id) AS joined FROM group_members WHERE member=? AND group_id=? LIMIT 1',
      [user, group]
    );
    return db.tf(is[0].joined);
  } catch (error) {
    console.error('Error in joinedGroup:', error);
    return false;
  }
};

/**
 * Returns mutual users between group members and a user
 * @param {Number} user UserID
 * @param {Number} group GroupID
 */
const mutualGroupMembers = async (user, group) => {
  try {
    const myFollowings = await db.query(
      'SELECT follow_system.follow_to AS user, follow_system.follow_to_username AS username FROM follow_system WHERE follow_system.follow_by=?',
      [user]
    );
    const grpMembers = await db.query(
      'SELECT group_members.member AS user, users.username AS username FROM group_members, users WHERE group_id = ? AND group_members.member = users.id ORDER BY group_members.joined_group DESC',
      [group]
    );

    const mutuals = intersectionBy(myFollowings, grpMembers, 'user');
    return mutuals;
  } catch (error) {
    console.error('Error in mutualGroupMembers:', error);
    return [];
  }
};

module.exports = {
  getWhatOfGrp,
  deleteGroup,
  joinedGroup,
  mutualGroupMembers,
};
