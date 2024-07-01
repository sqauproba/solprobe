// Package auth provides JWT signing, verification, and API-key helpers.
package auth

import (
	"crypto/rand"
	"encoding/base64"
	"errors"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

// Claims is the JWT claims struct used by SolProbe.
type Claims struct {
	ClientID string   `json:"cid"`
	Scopes   []string `json:"scopes"`
	jwt.RegisteredClaims
}

// Sign creates a signed JWT for a client with the given scopes.
func Sign(secret string, clientID string, scopes []string, ttl time.Duration) (string, error) {
	claims := Claims{
		ClientID: clientID,
		Scopes:   scopes,
		RegisteredClaims: jwt.RegisteredClaims{
			Subject:   clientID,
			Issuer:    "solprobe-api",
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(ttl)),
		},
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(secret))
}

// Verify parses and validates a JWT, returning its claims.
func Verify(secret, tokenString string) (*Claims, error) {
	claims := &Claims{}
	token, err := jwt.ParseWithClaims(
		tokenString,
		claims,
		func(t *jwt.Token) (any, error) {
			if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, errors.New("unexpected signing method")
			}
			return []byte(secret), nil
		},
	)
	if err != nil {
		return nil, err
	}
	if !token.Valid {
		return nil, errors.New("invalid token")
	}
	return claims, nil
}

// GenerateAPIKey returns a new random API key with the given prefix.
func GenerateAPIKey(prefix string) (string, error) {
	buf := make([]byte, 32)
	if _, err := rand.Read(buf); err != nil {
		return "", err
	}
	return prefix + base64.RawURLEncoding.EncodeToString(buf), nil
}
