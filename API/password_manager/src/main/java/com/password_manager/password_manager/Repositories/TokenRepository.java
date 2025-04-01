package com.password_manager.password_manager.Repositories;

import com.password_manager.password_manager.models.TokenModel;
import com.password_manager.password_manager.models.UserModel;
import jakarta.transaction.Transactional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface TokenRepository extends JpaRepository<TokenModel, Long> {
    Optional<TokenModel> findByToken(String token);
    @Modifying
    @Transactional
    void deleteByUser( UserModel user);
}
