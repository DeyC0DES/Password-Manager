package com.password_manager.password_manager.config.security;

import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.JWT;
import com.auth0.jwt.exceptions.JWTCreationException;
import com.auth0.jwt.exceptions.JWTVerificationException;
import com.password_manager.password_manager.Repositories.TokenRepository;
import com.password_manager.password_manager.models.TokenModel;
import com.password_manager.password_manager.models.UserModel;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;

@Service
public class TokenService {

    private final TokenRepository tokenRepository;

    @Value("${spring.security.secret.key}")
    private String secret;

    public TokenService(TokenRepository tokenRepository) {
        this.tokenRepository = tokenRepository;
    }

    public String validateToken(String token) {
        Algorithm algorithm = Algorithm.HMAC256(secret);
        try {
            String email = JWT.require(algorithm)
                    .build()
                    .verify(token)
                    .getSubject();

            TokenModel tokenStored = tokenRepository.findByToken(token).orElse(null);

            if (tokenStored != null && tokenStored.isActive()) {
                return email;
            }

            return null;

        } catch (JWTVerificationException e) {
            return null;
        }
    }

    public String generateToken(UserModel userModel) {
        Algorithm algorithm = Algorithm.HMAC256(secret);
        try {
            String newToken = JWT.create()
                    .withIssuer("password-manager-API")
                    .withSubject(userModel.getEmail())
                    .withExpiresAt(generateExpireAt())
                    .sign(algorithm);

            tokenRepository.deleteByUser(userModel);

            TokenModel tokenModel = new TokenModel();
            tokenModel.setToken(newToken);
            tokenModel.setUser(userModel);
            tokenRepository.save(tokenModel);

            return newToken;
        } catch (JWTCreationException e) {
            throw new RuntimeException("Error while generate: Creation: " + e.getMessage(), e);
        }
    }

    public Instant generateExpireAt() {
        return LocalDateTime.now().plusHours(24).toInstant(ZoneOffset.UTC);
    }

}
