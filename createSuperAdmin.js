const admin = require('firebase-admin');

// IMPORTANT: You must download your Service Account Key from the Firebase Console:
// Project Settings > Service Accounts > Generate new private key
// Save it in the same folder as this script and name it "serviceAccountKey.json"
const serviceAccount = require('./serviceAccountKey.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();

// The designated Super Admin email
const SUPER_ADMIN_EMAIL = 'connect.thesode@gmail.com';

async function setupSuperAdmin() {
  console.log(`Setting up Super Admin for: ${SUPER_ADMIN_EMAIL}...`);
  
  let userRecord;
  try {
    userRecord = await admin.auth().getUserByEmail(SUPER_ADMIN_EMAIL);
    console.log(`User already exists in Auth with UID: ${userRecord.uid}`);
  } catch (error) {
    if (error.code === 'auth/user-not-found') {
      console.log('User not found. Creating new Firebase Auth user...');
      userRecord = await admin.auth().createUser({
        email: SUPER_ADMIN_EMAIL,
        emailVerified: true
      });
      console.log(`Created new user with UID: ${userRecord.uid}`);
    } else {
      console.error('Error fetching user:', error);
      process.exit(1);
    }
  }

  try {
    console.log('Assigning superadmin custom claim...');
    await admin.auth().setCustomUserClaims(userRecord.uid, { role: 'superadmin' });
    console.log('Custom claims assigned successfully.');

    console.log('Creating adminMeta document...');
    await db.collection('adminMeta').doc(userRecord.uid).set({
      role: 'superadmin',
      needsPasswordReset: false,
      invitedAt: admin.firestore.FieldValue.serverTimestamp(),
      invitedBy: 'system'
    });
    console.log('adminMeta document created successfully.');

    console.log('\n✅ Setup Complete!');
    console.log(`You can now log into the admin panel using Google Sign-In with ${SUPER_ADMIN_EMAIL}.`);
    process.exit(0);
  } catch (error) {
    console.error('Error during setup:', error);
    process.exit(1);
  }
}

setupSuperAdmin();
