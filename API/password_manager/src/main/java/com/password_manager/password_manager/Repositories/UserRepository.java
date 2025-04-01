package com.password_manager.password_manager.Repositories;

import com.password_manager.password_manager.models.UserModel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface UserRepository extends JpaRepository<UserModel, UUID> {
    Optional<UserModel> findById(UUID id);
    Optional<UserModel> findByEmail(String email);
}
