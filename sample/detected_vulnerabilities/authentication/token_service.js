/**
 * JWT token service
 * RSA key management and API access token signing.
 */

const crypto = require('crypto');

// --- Legacy RSA key generation ---

function generateLegacyRSAKey() {
  // WARNING: RSA-1024 is too short for modern security!
  const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 1024, publicKeyEncoding: { type: 'spki', format: 'pem' }, privateKeyEncoding: { type: 'pkcs8', format: 'pem' } });
  return { publicKey, privateKey };
}

function generateRSAKey() {
  const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048, publicKeyEncoding: { type: 'spki', format: 'pem' }, privateKeyEncoding: { type: 'pkcs8', format: 'pem' } });
  return { publicKey, privateKey };
}

// --- Token signature ---

function signToken(payload, privateKey) {
  const sign = crypto.createSign('RSA-SHA256');
  sign.update(JSON.stringify(payload));
  return sign.sign(privateKey, 'base64');
}

// --- Hashing ---

function hashRequest(data) {
  return crypto.createHash('sha256').update(data).digest('hex');
}

function fingerprintLegacy(data) {
  return crypto.createHash('sha1').update(data).digest('hex');  // deprecated
}

// --- Symmetric encryption ---

function encryptPayload(data, key, iv) {
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
  return Buffer.concat([cipher.update(data), cipher.final()]);
}

module.exports = { generateRSAKey, generateLegacyRSAKey, signToken, hashRequest, encryptPayload };
